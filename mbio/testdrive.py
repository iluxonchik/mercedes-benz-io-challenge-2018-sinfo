"""Code that loads the dataset and handles queries on it."""
import json
import uuid
import datetime
from collections import defaultdict, OrderedDict
from mbio.utils import is_str_equal_ignore_case
from mbio.geo.coordinate import Coordinate
from mbio.date.bookingdate import BookingDate, BookingResponse
from mbio.exceptions import (InvalidDataSetError,  VehicleNotFoundError,
                    VehicleAlreadyBookedError, VehicleNotAvailableOnDateError,
                    BookingError, BookingDoesNotExistError, BookingAlreadyCancelledError,
                    DatasetNotFoundError)

class TestDrive(object):

    def __init__(self, dataset):
        self._dataset_path = dataset
        self._dataset = self._load_dataset(self._dataset_path)

    def get_vehicles_by_attributes(self, dealer=None, model=None, fuel=None, transmission=None):
        vehicles = list(self._all_vehicles)

        if dealer is not None:
            vehicles = self.get_vehicles_by_dealer(dealer, vehicles)
        if model is not None:
            vehicles = self.get_vehicles_by_model(model, vehicles)
        if fuel is not None:
            vehicles = self.get_vehicles_by_fuel_type(fuel, vehicles)
        if transmission is not None:
            vehicles = self.get_vehicles_by_transmission(transmission, vehicles)

        return vehicles

    def get_vehicles_by_model(self, model, vehicles=None):
        """
        Returns a list of vehicles with the specified model.
        """
        vehicles = vehicles if vehicles is not None else self._all_vehicles

        return self._filter_vehicles_by_property_value('model', model, vehicles)

    def get_vehicles_by_fuel_type(self, fuel, vehicles=None):
        vehicles = vehicles if vehicles is not None else self._all_vehicles

        return self._filter_vehicles_by_property_value('fuel', fuel, vehicles)

    def get_vehicles_by_transmission(self, transmission, vehicles=None):
        vehicles = vehicles if vehicles is not None else self._all_vehicles

        return self._filter_vehicles_by_property_value('transmission',
                                                       transmission, vehicles)

    def get_vehicles_by_dealer(self, dealer, vehicles=None):
        vehicles = vehicles if vehicles is not None else self._all_vehicles

        for mb_dealer in self._dataset['dealers']:
            if mb_dealer['id'].lower() == dealer.lower():
                return mb_dealer['vehicles']
        return []

    def get_closest_dealer_with_vehicle(self, latitude, longitude, model=None,
                                            fuel=None, transmission=None):
        sorted_dealers = self._sort_dealers_by_distance(latitude, longitude)
        for dealer_group in sorted_dealers:
            for dealer in dealer_group:
                if self._dealer_has_vehicle(dealer, model, fuel, transmission):
                    return dealer
        return None

    def get_dealers_in_polugon_with_vehicle(self, coord_pair, model=None, fuel=None,
                                        transmission=None):

        res = []
        polygon = [Coordinate(*lat_lon_pair) for lat_lon_pair in coord_pair]
        for dealer in self._dataset['dealers']:
            if self._dealer_has_vehicle(dealer, model, fuel, transmission):
                dealer_coord = Coordinate(dealer['latitude'], dealer['longitude'])
                if dealer_coord.is_inside_polygon(polygon):
                    res.append(dealer)
        return res



    def get_closest_dealers_with_vehicle(self, latitude, longitude, model=None,
                                            fuel=None, transmission=None):
        res = []
        sorted_dealers = self._sort_dealers_by_distance(latitude, longitude)
        for dealer_group in sorted_dealers:
            for dealer in dealer_group:
                if self._dealer_has_vehicle(dealer, model, fuel, transmission):
                    res += [dealer]
        return res

    def create_booking(self, first_name, last_name, vehicle_id, pickup_date):
        vehicles_with_id = self._filter_vehicles_by_property_value('id', vehicle_id)
        assert len(vehicles_with_id) < 2, 'More than one vehicles with the same id.'

        if len(vehicles_with_id) < 1:
            raise VehicleNotFoundError('Vehicle with id {} was not found'.format(vehicle_id))
        vehicle = vehicles_with_id[0]
        bookings = self._dataset['bookings']
        booking_date = BookingDate(pickup_date)
        booking_result = booking_date.is_booking_possible(vehicle, bookings)

        booking_possible = booking_result.is_success
        if booking_possible:
            # all good, create a booking, and add it to bookings
            new_booking = self._create_booking(first_name, last_name,
                            vehicle_id, pickup_date, vehicle, bookings)
            return new_booking

        # here we know that hte booking is not possible, let's check the reason
        error_code = booking_result.error_code
        # if the error code has not been set, something went wrong
        assert error_code is not None, 'Error code has not been set'

        if error_code is BookingResponse.ERR_CAR_DATE:
            msg = 'The requested vehicle is not available on {}'.format(pickup_date.isoformat())
            raise VehicleNotAvailableOnDateError(msg)
        elif error_code is BookingResponse.ERR_BOOKING_EXITS:
            msg = 'Booking for {} already exists'.format(pickup_date.isoformat())
            raise VehicleAlreadyBookedError(msg)
        else:
            # somehting else went wrong, this shouldn't realy happen, but
            # let's not let the app crash here
            raise BookingError('Could not create booking.')

    def cancel_booking(self, booking_id, reason):
        booking = self._get_booking(booking_id)

        if booking is None:
            msg = 'Booking with id {} does not exist'.format(booking_id)
            raise BookingDoesNotExistError(msg)

        # check if booking was already cancelled
        if 'cancelledAt' in booking:
            msg = 'Booking with id {} has already been cancelled'.format(booking_id)
            raise BookingAlreadyCancelledError(msg)

        booking['cancelledAt'] = datetime.datetime.today().isoformat()
        booking['cancelledReason'] = reason

        return booking

    def _get_booking(self, booking_id):
        for booking in self._dataset['bookings']:
            if is_str_equal_ignore_case(booking['id'], booking_id):
                return booking
        return None

    def _create_booking(self, first_name, last_name, vehicle_id, pickup_date, vehicle, bookings):
        new_booking = self._create_booking_obj(first_name, last_name, vehicle_id, pickup_date)
        # insert booking into db
        bookings.append(new_booking)
        return new_booking


    def _create_booking_obj(self, first_name, last_name, vehicle_id, pickup_date):
        booking = {
                    'id': str(uuid.uuid4()),
                    'firstName': first_name,
                    'lastName': last_name,
                    'vehicleId': vehicle_id,
                    'pickupDate': pickup_date.isoformat(),
                    'createdAt': datetime.datetime.today().isoformat()
        }
        return booking


    def _sort_dealers_by_distance(self, latitude, longitude):
        my_coord = Coordinate(latitude, longitude)
        sorted_dealers = defaultdict(list)
        # go through the dealers list and compute the distances
        for dealer in self._dataset['dealers']:
            dealer_coord = Coordinate(dealer['latitude'], dealer['longitude'])
            distance = my_coord.distance_to(dealer_coord)
            sorted_dealers[distance].append(dealer)
        sorted_dealers = OrderedDict(sorted(sorted_dealers.items()))
        sorted_dealers = [dealer for dealer in sorted_dealers.values()]
        return sorted_dealers


    @property
    def _all_vehicles(self):
        """
        Iterator over the list of all vehicles in the dataset.
        """
        for dealer in self._dataset['dealers']:
            for vehicle in dealer['vehicles']:
                yield vehicle

    def _load_dataset(self, path):
        try:
            with open(path, 'r') as f:
                try:
                    dataset = json.load(f)
                except json.JSONDecodeError:
                    msg = 'Error in when decoding JSON file: {}'.format(path)
                    raise InvalidDataSetError(msg)
            return dataset
        except FileNotFoundError:
            msg = 'Dataset at {} not found. Make sure that the file path is correct.'.format(path)
            raise DatasetNotFoundError(msg)


    def _filter_vehicles_by_property_value(self, name, value, vehicles=None):
        """
        Filter vehicles by the value of their property.
        """
        vehicles = vehicles if vehicles is not None else self._all_vehicles

        res = []
        for vehicle in vehicles:
            if is_str_equal_ignore_case(vehicle[name], value):
                res += [vehicle]
        return res

    def _dealer_has_vehicle(self, dealer, model, fuel, transmission):
        vehicles = dealer['vehicles']
        for vehicle in vehicles:
            if model is not None:
                if not is_str_equal_ignore_case(vehicle['model'], model):
                    continue
            if fuel is not None:
                if not is_str_equal_ignore_case(vehicle['fuel'], fuel):
                    continue
            if transmission is not None:
                if not is_str_equal_ignore_case(vehicle['transmission'], transmission):
                    continue
            return True
        return False
