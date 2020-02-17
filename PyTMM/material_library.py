import os
import sys
from io import open
from pathlib import Path

import numpy
import scipy.interpolate
import yaml


DATA_BASE_PATH = Path(__file__).parent.parent / (
    "externals/glass_database/database/data")


class MaterialLibrary:
    """Class that parses the refractiveindex.info YAML database
    """

    def __init__(self, data_base_path=DATA_BASE_PATH):
        """constructor for a MaterialLibrary object

        :param data_base_path:
        """
        self.data_path = Path(data_base_path)
        if not self.data_path.exists():
            raise ValueError('The data base path does not exist.')
        fname = self.data_path.parent / "library.yml"
        with open(fname, "rt", encoding="utf-8") as lib_yml:
            self.catalog = yaml.safe_load(lib_yml)

    def get_material_file(self, shelf, book, page):
        """
        :param shelf:
        :param book:
        :param page:
        :return:
        """
        for shelf_iter in self.catalog:
            if shelf_iter['SHELF'] == shelf:
                break
        else:
            # is executed if no break occurs.
            print(f'shelf "{shelf}" not found.')

        for book_iter in shelf_iter['content']:
            try:
                if book_iter['BOOK'] == book:
                    break
            except KeyError:  # DIVIDER
                pass
        else:
            print(f'book "{book}" not found.')

        for page_iter in book_iter['content']:
            try:
                if page_iter['PAGE'] == page:
                    return self.data_path / page_iter['data']
            except KeyError:  # DIVIDER
                pass
        raise FileNotFoundError(
            f'Material file not found with parameters:'
            f' shelf={shelf},'
            f' book={book},'
            f' page={page}')
