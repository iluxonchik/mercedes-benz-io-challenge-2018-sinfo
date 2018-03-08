"""Code that loads the dataset and handles queries on it."""
import json
from mbio.exceptions import InvalidDataSetError

class TestDrive(object):

    def __init__(self, dataset):
        self._dataset_path = dataset
        self._dataset = self._load_dataset(self._dataset_path)

    def get_vehicles_by_model(self, model):
        res = []
        for dealer in self._dataset['dealers']:
            for vehicle in dealer['vehicles']:
                if vehicle['model'].lower() == model.lower():
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
