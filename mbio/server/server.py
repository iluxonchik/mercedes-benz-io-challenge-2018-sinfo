"""
HTTP server that handles the request from the client application.
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from locmess.decorators import handle_expcetions

logging.basicConfig(level=logging.DEBUG)

# User related
NEW_USER = '/new/user'  # {username, password}
LOGIN = '/login'  # {username, password}
LOGOUT = '/logout' # {username, token}

# Location related
NEW_LOCATION =  '/new/location'  # {username, token, name, is_gps, location_json}
GET_LOCATION = '/get/location'   # {username, token, name}

# Message realted
NEW_MESSAGE = '/new/message'  # {username, token, title, location_name, text, is_centralized, is_black_list, properties, valid_from?, valid_until?, is_visible?}
GET_GPS_MESSAGES = '/get/message/gps' # {username, token, curr_coord}

lm = LocMess()

# HTTPRequestHandler class
class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        logging.debug(self.path)
        logging.debug(self.headers['content'])
        path = self.path
        json_content = self.headers['content']

        json_dict = json.loads(json_content)
        logging.debug('Loaded json: ')
        logging.debug(json_dict)

    def do_POST(self):
        logging.debug(self.path)
        logging.debug(self.headers['content'])
        path = self.path
        json_content = self.rfile.read(int(self.headers['Content-Length']))

        logging.debug('Raw Content')
        logging.debug(json_content)

        json_dict = json.loads(json_content)
        logging.debug('Loaded json: ')
        logging.debug(json_dict)

        if LOGIN in path:
            self.login(json_dict)
        if NEW_USER in path:
            self.add_user(json_dict)
        if LOGOUT in path:
            self.logout(json_dict)
        if NEW_LOCATION in path:
            self.add_location(json_dict)
        if GET_LOCATION in path:
            self.get_location(json_dict)
        if NEW_MESSAGE in path:
            self.add_message(json_dict)
        if GET_GPS_MESSAGES in path:
            self.get_gps_messages(json_dict)


    @handle_expcetions
    def login(self, args):
        token = lm.login(args['username'], args['password'])

        if token is None:
                self.send_response(401)
                self.send_header('Content-type','text/html')
                self.end_headers()
                return

        ret_json = {'token':token.decode()}
        self._send_OK_headers()
        self._respond_json(ret_json)


    @handle_expcetions
    def add_user(self, args):
        lm.add_user(args['username'], args['password'])
        self._send_OK_headers()

    @handle_expcetions
    def logout(self, args):
        lm.logout(args['username'], args['token'].encode())
        self._send_OK_headers()

    @handle_expcetions
    def add_location(self, args):
        # {username, token, name, is_gps, location_json }
        username, token = self._parse_auth(args)
        name, is_gps, location_json = args['name'], args['is_gps'], args['location_json']
        lm.add_location(username, token, name, is_gps, location_json)
        self._send_OK_headers()

    @handle_expcetions
    def get_location(self, args):
        # { username, token, name }
        logging.info('# get_location #')
        username, token = self._parse_auth(args)
        name = args['name']
        location = lm.get_location_by_name(username, token, name)
        res_dict = {
                        'name': location.name,
                        'author': location.author.username,
                        'is_gps': location.is_gps,
                        'location': location.location,
                   }
        logging.info('\t* replying with dict:')
        logging.info('\t\t{}'.format(res_dict))

        self._respond_json(res_dict)

    @db_session
    @handle_expcetions
    def add_message(self, args):
         # {
         #    username, token, title, location_name, text, is_centralized,
         #    is_black_list, properties, valid_from?, valid_until?, is_visible?
         # }
         username, token = self._parse_auth(args)
         title = args['title']
         location_name = args['location_name']
         location = None
         with db_session:
             location = lm.get_location_by_name(username, token, location_name)
         text = args['text']
         is_centralized = args['is_centralized']
         is_black_list = args['is_black_list']
         properties = args['properties']

         valid_from = None
         try:
             valid_from = args['valid_from']
             valid_from = dateutil.parser.parse(valid_from)
         except KeyError as e:
             pass

         valid_until = None
         try:
             valid_until = args['valid_from']
             valid_until = dateutil.parser.parse(valid_until)
         except KeyError as e:
             pass

         is_visible = None
         try:
             is_visible = args['valid_from']
         except KeyError as e:
             pass

         lm.add_message(username, token,
         title=title, location=location,
         text=text, is_centralized=is_centralized, is_black_list=is_black_list,
         valid_from=valid_from, valid_until=valid_until, properties=properties)

         self._send_OK_headers()


    @handle_expcetions
    def get_gps_messages(self, args):
        # { username, token, curr_coord }

        username, token = self._parse_auth(args)
        curr_coord = args['curr_coord']

        msgs = lm.get_available_messages_by_gps(username, token, curr_coord)
        json_msgs = [json.dumps(self._msg_to_json_dict(msg)) for msg in msgs]
        msgs_dict = {
                        'messages': json_msgs
                    }
        self._respond_json(msgs_dict)


    def _msg_to_json_dict(self, msg_obj):
        msg_dict = {
                        'author': msg_obj.author.username,
                        'title': msg_obj.title,
                        'location': msg_obj.location.location,
                        'text': msg_obj.text,
                        'is_centralized': msg_obj.is_centralized,
                        'is_black_list': msg_obj.is_black_list,
                        'valid_from': msg_obj.valid_from.isoformat(),
                        'valid_until': msg_obj.valid_until.isoformat(),
                        'time_posted': msg_obj.time_posted.isoformat(),
                        'properties': msg_obj.properties,
                        'is_visible': msg_obj.is_visible
                   }
        return msg_dict

    def _respond_json(self, json_dict):
        self._send_OK_headers()
        res = json.dumps(json_dict)
        self.wfile.write(res.encode())

    def _send_OK_headers(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

    def _parse_auth(self, args):
        return (args['username'], args['token'].encode())
