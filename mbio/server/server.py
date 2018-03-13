"""
HTTP server that handles the request from the client application.
"""
import sys
import json
import logging
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler

from mbio.server.endpoint import Endpoint
from mbio.testdrive import TestDrive
from mbio.server.decorators import handle_expcetions
from mbio.date.utils import isoformat_to_datetime

from mbio.exceptions import (VehicleNotFoundError, VehicleNotAvailableOnDateError,
                        VehicleAlreadyBookedError, BookingError, BookingDoesNotExistError,
                        BookingAlreadyCancelledError)

logging.basicConfig(level=logging.DEBUG)

class Server(BaseHTTPRequestHandler):

    DATASET_PATH = None
    HTTP_OK = 200
    HTTP_OK_CREATED = 201
    HTTP_BAD_REQUEST = 400

    METHOD_POST = 'POST'
    METHOD_GET = 'GET'
    METHOD_PUT = 'PUT'

    METHOD_ENDPOINTS = {
        METHOD_GET: [Endpoint.VEHICLES, Endpoint.DEALER_CLOSEST,
                     Endpoint.DEALERS_CLOSEST_LIST,
                     Endpoint.DEALERS_IN_POLYGON],
        METHOD_POST: [Endpoint.BOOKINGS_CREATE],
        METHOD_PUT: [Endpoint.BOOKINGS_CANCEL],
    }


    td = None

    def __init__(self, *args, **kwargs):
        # NOTE: do all of the setup and then call the super's __init__.
        # After digging into the source code, I found out that BaseRequestHandler
        # (parent of BaseHTTPRequestHandler) calls handle() in its constructor,
        # so that means that the overriden do_* methods will be called straight
        # away, beofore running any other code in Server's __init__.
        # https://github.com/python/cpython/blob/master/Lib/socketserver.py#L695
        self.RES_FUNC = {
            Endpoint.VEHICLES: self.get_vehicles,

            Endpoint.DEALERS_CLOSEST_LIST: self.get_closest_dealers_list,
            Endpoint.DEALER_CLOSEST: self.get_closest_dealer,
            Endpoint.DEALERS_IN_POLYGON: None,

            Endpoint.BOOKINGS_CREATE: self.create_booking,
            Endpoint.BOOKINGS_CANCEL: self.cancel_booking,
        }
        self._init_td_if_needed()
        super(Server, self).__init__(*args, **kwargs)

    def _init_td_if_needed(self):
        if Server.td is None:
            try:
                Server.td = TestDrive('./tests/resources/dataset_full.json')
            except Exception as e:
                print('[!!!] Fatal error occured. The application will end.')
                print('\t{}'.format(str(e)))
                sys.exit(-1)

    @handle_expcetions
    def do_GET(self):
        logging.debug(self.path)
        logging.debug(self.headers['content'])

        query_params = self._parse_query_params_and_endpoint(self.path)
        endpoint = query_params['endpoint']

        is_valid = self._is_valid_endpoint_method(endpoint, Server.METHOD_GET)
        if not is_valid:
            return

        dispatch_function = self.RES_FUNC.get(endpoint, self.invalid_endpoint_err)
        dispatch_function(query_params)

    @handle_expcetions
    def do_POST(self):
        query_params = self._parse_request_json(self.path)
        endpoint = query_params['endpoint']

        is_valid = self._is_valid_endpoint_method(endpoint, Server.METHOD_POST)
        if not is_valid:
            return

        dispatch_function = self.RES_FUNC.get(endpoint, self.invalid_endpoint_err)
        dispatch_function(query_params)

    @handle_expcetions
    def do_PUT(self):
        query_params = self._parse_request_json(self.path)
        endpoint = query_params['endpoint']

        is_valid = self._is_valid_endpoint_method(endpoint, Server.METHOD_PUT)
        if not is_valid:
            return

        dispatch_function = self.RES_FUNC.get(endpoint, self.invalid_endpoint_err)
        dispatch_function(query_params)

    def _is_valid_endpoint_method(self, endpoint, curr_method):
        if curr_method is Server.METHOD_POST:
            return self._validate_is_post_only(endpoint)
        if curr_method is Server.METHOD_GET:
            return self._validate_is_get_only(endpoint)
        if curr_method is Server.METHOD_PUT:
            return self._validate_is_put_only(endpoint)

        return True

    def _validate_is_get_only(self, endpoint):
        if endpoint not in Server.METHOD_ENDPOINTS[Server.METHOD_GET]:
            msg = self._get_endpoint_err_msg(endpoint)
            err = self._build_error_dict(msg)
            self._respond_json(err, self.HTTP_BAD_REQUEST)
            return False
        return True

    def _validate_is_post_only(self, endpoint):
        if endpoint not in Server.METHOD_ENDPOINTS[Server.METHOD_POST]:
            msg = self._get_endpoint_err_msg(endpoint)
            err = self._build_error_dict(msg)
            self._respond_json(err, self.HTTP_BAD_REQUEST)
            return False
        return True

    def _validate_is_put_only(self, endpoint):
        if endpoint not in Server.METHOD_ENDPOINTS[Server.METHOD_PUT]:
            msg = self._get_endpoint_err_msg(endpoint)
            err = self._build_error_dict(msg)
            self._respond_json(err, self.HTTP_BAD_REQUEST)
            return
        return True

    def _get_endpoint_err_msg(self, endpoint):
        msg = 'Unknown endpoint.'
        for key in Server.METHOD_ENDPOINTS:
            if endpoint in Server.METHOD_ENDPOINTS[key]:
                msg = 'This endpoint only supports the {} method.'.format(key)
                break
        return msg

    def _parse_request_json(self, path):
        logging.debug(self.path)
        logging.debug(self.headers['content'])
        json_content = self.rfile.read(int(self.headers['Content-Length']))

        logging.debug('Raw Content')
        logging.debug(json_content)

        query_params = json.loads(json_content)
        logging.debug('Loaded json: ')
        logging.debug(query_params)

        parsed_url = urlparse(path)
        path = parsed_url.path
        path = self._normalize_path(path)
        query_params['endpoint'] = path

        return query_params

    def invalid_endpoint_err(self, args):
        endpoint = args['endpoint']
        err = self._build_error_dict('{} is not a valid endpoint'.format(endpoint))
        self._respond_json(err, self.HTTP_BAD_REQUEST)

    @handle_expcetions
    def get_vehicles(self, args):
        dealer = args.get('dealer', None)
        model = args.get('model', None)
        fuel = args.get('fuel', None)
        transmission = args.get('transmission', None)

        vehicles = Server.td.get_vehicles_by_attributes(dealer=dealer, model=model, fuel=fuel, transmission=transmission)

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

        res = Server.td.get_closest_dealers_with_vehicle(latitude, longitude, model, fuel, transmission)

        res_json = {'dealers': res}
        self._respond_json(res_json, self.HTTP_OK)

    @handle_expcetions
    def get_closest_dealer(self, args):
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

        res = Server.td.get_closest_dealer_with_vehicle(latitude, longitude, model, fuel, transmission)

        res_json = {'dealer': res}
        self._respond_json(res_json, self.HTTP_OK)

    @handle_expcetions
    def create_booking(self, args):
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        vehicle_id = args.get('vehicle_id', None)
        pickup_date = args.get('pickup_date', None)

        if None in (first_name, last_name, vehicle_id, pickup_date):
            self._respond_API_error(msg='fist_name, last_name, vehicle_id and pickup_date parameters are ALL required')
            return

        # 1. Try and parse the date, if error, send err message
        try:
            pickup_date_dt_obj = isoformat_to_datetime(pickup_date)
        except ValueError:
            err = self._build_error_dict('{} is not a valid ISO date format')
            self._respond_json(err, self.HTTP_BAD_REQUEST)
            return

        try:
            res = Server.td.create_booking(first_name, last_name, vehicle_id, pickup_date_dt_obj)
        except (VehicleNotFoundError, VehicleNotAvailableOnDateError,
                                VehicleAlreadyBookedError, BookingError) as e:
            err = self._build_error_dict(str(e))
            self._respond_json(err, self.HTTP_BAD_REQUEST)
            return

        # Okay, everything went fine, so let's respond with the new booking
        self._respond_json(res, self.HTTP_OK_CREATED)

    @handle_expcetions
    def cancel_booking(self, args):
        booking_id = args.get('booking_id', None)
        reason = args.get('reason', None)

        if None in (booking_id, reason):
            self._respond_API_error(msg='booking id and reason parameters are required')
            return

        try:
            res = Server.td.cancel_booking(booking_id, reason)
        except (BookingDoesNotExistError, BookingAlreadyCancelledError) as e:
            err_res = self._build_error_dict(str(e))
            self._respond_json(err_res, self.HTTP_BAD_REQUEST)
            return

        self._respond_json(res, self.HTTP_OK)



    def _respond_API_error(self, msg):
        res_dict = self._build_error_dict(msg)
        self._respond_json(res_dict, self.HTTP_BAD_REQUEST)


    def _parse_query_params_and_endpoint(self, path):
        res = {}
        parsed_url = urlparse(path)
        query_dict = parse_qs(parsed_url.query)
        for key, value in query_dict.items():
            res[key] = value[0]

        path = parsed_url.path
        path = self._normalize_path(path)
        res['endpoint'] = path

        return res

    def _normalize_path(self, path):
        if not path.endswith('/'):
            path = '{}/'.format(path)
        return path

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
