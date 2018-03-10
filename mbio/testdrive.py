"""Code that loads the dataset and handles queries on it."""
import json
from collections import defaultdict, OrderedDict
from mbio.utils import is_str_equal_ignore_case
from mbio.geo.coordinate import Coordinate
from mbio.exceptions import InvalidDataSetError

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
        """
        Sort dealers by distance
        Foreach sorted dealer:
            if dealer has vehicle with attrs, return
        If all dealers have been passed through, return None
        """
        sorted_dealers = self._sort_dealers_by_distance(latitude, longitude)
        for dealer_group in sorted_dealers:
            for dealer in dealer_group:
                if self._dealer_has_vehicle(dealer, model, fuel, transmission):
                    return dealer
        return None

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
