"""Code that loads the dataset and handles queries on it."""
import json
from mbio.exceptions import InvalidDataSetError

class TestDrive(object):

    def __init__(self, dataset):
        self._dataset_path = dataset
        self._dataset = self._load_dataset(self._dataset_path)

    @property
    def all_vehicles(self):
        """
        Iterator over the list of all vehicles in the dataset.
        """
        for dealer in self._dataset['dealers']:
            for vehicle in dealer['vehicles']:
                yield vehicle

    def get_vehicles_by_model(self, model):
        """
        Returns a list of vehicles with the specified model.
        """
        res = []
        for vehicle in self.all_vehicles:
            if vehicle['model'].lower() == model.lower():
                res += [vehicle]
        return res

    def get_vehicles_by_fuel_type(self, fuel):
        res = []
        for vehicle in self.all_vehicles:
            if vehicle['fuel'].lower() == fuel.lower():
                res += [vehicle]
        return res

    def get_vehicles_by_transmission(self, transmission):
        res = []
        for vehicle in self.all_vehicles:
            if vehicle['transmission'].lower() == transmission.lower():
                res += [vehicle]
        return res

    def _load_dataset(self, path):

        with open(path, 'r') as file:
            try:
                dataset = json.load(file)
            except json.JSONDecodeError:
                msg = f'Error in when decoding JSON file: {path}'
                raise InvalidDataSetError(msg)

        return dataset
