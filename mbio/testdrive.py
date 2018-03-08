"""Code that loads the dataset and handles queries on it."""
import json
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
            if vehicle[name].lower() == value.lower():
                res += [vehicle]
        return res
