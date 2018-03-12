"""
HTTP server that handles the request from the client application.
"""
import sys
import json
import logging
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

from mbio.testdrive import TestDrive
from mbio.server.decorators import handle_expcetions

logging.basicConfig(level=logging.DEBUG)

API_PREFIX = '/api/'
VEHICLES = API_PREFIX + 'vehicles'  # ?dealer=AAA?model=XXX?fuel=YYY?transmission=ZZZ

DEALERS_CLOSEST_LIST = API_PREFIX + 'dealers' # ?dealer=AAA?model=XXX?fuel=YYY?transmission=ZZZ?latitude=LLL?longitude=OOO
DEALER_CLOSEST = API_PREFIX + 'dealers/closest' # ?dealer=AAA?model=XXX?fuel=YYY?transmission=ZZZ?latitude=LLL?longitude=OOO
DEALERS_IN_POLYGON = API_PREFIX + 'dealers/polygon'

BOOKINGS_CREATE = API_PREFIX + '/bookings/create' # {first_name, last_name, vehicle_id, pickup_date}
BOOKINGS_CANCEL = API_PREFIX + '/booking/cancel' # {booking_id, reason}

# HTTPRequestHandler class
class Server(BaseHTTPRequestHandler):

    DATASET_PATH = None
    HTTP_OK = 200

    def __init__(self, *args, **kwargs):
        # NOTE: do all of the setup and then call the super's __init__.
        # After digging into the source code, I found out that BaseRequestHandler
        # (parent of BaseHTTPRequestHandler) calls handle() in its constructor,
        # so that means that the overriden do_* methods will be called straight
        # away, beofore running any other code in Server's __init__.
        # https://github.com/python/cpython/blob/master/Lib/socketserver.py#L695
        self.RES_FUNC = {
            VEHICLES: self.get_vehicles,

            DEALERS_CLOSEST_LIST: self.get_closest_dealers_list,
            DEALER_CLOSEST: None,
            DEALERS_IN_POLYGON: None,

            BOOKINGS_CREATE: None,
            BOOKINGS_CANCEL: None,
        }

        try:
            self._td = TestDrive(self.DATASET_PATH)
        except Exception as e:
            print('[!!!] Fatal error occured. The application will end.')
            print('\t{}'.format(str(e)))
            sys.exit(-1)
        super(Server, self).__init__(*args, **kwargs)


    def do_GET(self):
        logging.debug(self.path)
        logging.debug(self.headers['content'])
        path = self.path
        json_content = self.headers['content']

        query_params, endpoint = self._parse_query_params_and_endpoint(self.path)
        query_params['endpoint'] = endpoint

        dispatch_function = self.RES_FUNC.get(endpoint, self.invalid_endpoint_err)
        dispatch_function(query_params)

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

        dispatch_function = self.RES_FUNC.get(self.path, self.invalid_endpoint_err)
        dispatch_function(json_dict)


    def invalid_endpoint_err(self, args):
        endpoint = args['endpoint']
        self._send_UNAUTH_headers('\'{}\' is an invalid endpoint.'.format(endpoint))

    @handle_expcetions
    def get_vehicles(self, args):
        dealer = args.get('dealer', None)
        model = args.get('model', None)
        fuel = args.get('fuel', None)
        transmission = args.get('transmission', None)

        vehicles = self._td.get_vehicles_by_attributes(dealer=dealer, model=model, fuel=fuel, transmission=transmission)

        ret_json = {'vehicles': vehicles}
        self._respond_json(ret_json, self.HTTP_OK)

    @handle_expcetions
    def get_closest_dealers_list(self, args):
        model = args.get('model', None)
        fuel = args.get('fuel', None)
        transmission = args.get('transmission', None)
        latitude = args.get('latitude', None)
        longitude = args.get('longitude', None)

        latitude = float(latitude) if latitude is not None else latitude
        longitude = float(longitude) if longitude is not None else longitude

        if None in (latitude, longitude):
            self._respond_API_error(msg='latitude and longitude parameters are required')
            return

        res = self._td.get_closest_dealers_with_vehicle(latitude, longitude, model, fuel, transmission)

        res_json = {'dealers': res}
        self._respond_json(res_json, self.HTTP_OK)

    def _respond_API_error(self, msg):
        res_dict = self._build_error_dict(msg)
        self._respond_json(res_dict, 400)


    def _parse_query_params_and_endpoint(self, path):
        res = {}
        parsed_url = urlparse(path)
        query_dict = parse_qs(parsed_url.query)
        for key, value in query_dict.items():
            res[key] = value[0]
        return res, parsed_url.path

    @handle_expcetions
    def delete_profile_key(self, args):
        username, token = self._parse_auth(args)
        key = args['key']
        lm.delete_key(username, token, key)
        self._send_OK_headers()

    def _respond_json(self, json_dict, code):
        self._send_response_headers(code)
        res = json.dumps(json_dict)
        self.wfile.write(res.encode())

    def _send_response_headers(self, code):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def _parse_auth(self, args):
        return (args['username'], args['token'].encode())

    def _build_error_dict(self, msg):
        return {'error': msg}
