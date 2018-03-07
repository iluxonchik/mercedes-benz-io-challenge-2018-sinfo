"""Code that loads the dataset and handles queries on it."""
import json
from mbio.exceptions import InvalidDataSetError

class TestDrive(object):

    def __init__(self, dataset):
        self._dataset_path = dataset
        self._datset = self._load_dataset(self._dataset_path)

    def _load_dataset(self, path):

        with open(path, 'r') as file:
            try:
                dataset = json.load(file)
            except json.JSONDecodeError:
                msg = f'Error in when decoding JSON file: {path}'
                raise InvalidDataSetError(msg)

        return dataset
