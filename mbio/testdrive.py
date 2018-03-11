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
                    BookingError)

class TestDrive(object):

    def __init__(self, dataset):
        self._dataset_path = dataset
        self._dataset = self._load_dataset(self._dataset_path)

    def get_vehicles_by_model(self, model):
        """
        Returns a list of vehicles with the specified model.
        """
        return self._filter_vehicles_by_property_value('model', model)

    def get_vehicles_by_fuel_type(self, fuel):
        return self._filter_vehicles_by_property_value('fuel', fuel)

    def get_vehicles_by_transmission(self, transmission):
        return self._filter_vehicles_by_property_value('transmission',
                                                       transmission)

    def get_vehicles_by_dealer(self, dealer):
        for mb_dealer in self._dataset['dealers']:
            if mb_dealer['name'].lower() == dealer.lower():
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


    def _create_booking(self, first_name, last_name, vehicle_id, pickup_date, vehicle, bookings):
        new_booking = self._create_booking_obj(first_name, last_name, vehicle_id, pickup_date)
        # insert booking into db
        bookings.append(new_booking)
        return new_booking


    def _create_booking_obj(self, first_name, last_name, vehicle_id, pickup_date):
        booking = {
                    'id': uuid.uuid4(),
                    'firstName': first_name,
                    'lastName': last_name,
                    'vehicleId': vehicle_id,
                    'pickupDate': pickup_date.isoformat(),
                    'createdAt': datetime.datetime.today()
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

        with open(path, 'r') as file:
            try:
                dataset = json.load(file)
            except json.JSONDecodeError:
                msg = f'Error in when decoding JSON file: {path}'
                raise InvalidDataSetError(msg)

        return dataset

    def _filter_vehicles_by_property_value(self, name, value):
        """
        Filter vehicles by the value of their property.
        """
        res = []
        for vehicle in self._all_vehicles:
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
