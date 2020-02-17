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
        """

        :param data_base_path:
        """
        self.data_path = Path(data_base_path)
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
        found = False
        for shelf_iter in self.catalog:
            if shelf_iter['SHELF'] == shelf:
                found = True
                break
        if not found:
            print(f'shelf "{shelf}" not found.')

        found = False
        for book_iter in shelf_iter['content']:
            try:
                if book_iter['BOOK'] == book:
                    found = True
                    break
            except KeyError:  # DIVIDER
                pass
        if not found:
            print(f'book "{book}" not found.')

        for page_iter in book_iter['content']:
            try:
                if page_iter['PAGE'] == page:
                    return self.data_path / page_iter['data']
            except KeyError:  # DIVIDER
                pass
        raise FileNotFoundError(
            f'Material file not found with parameters: shelf={shelf},'
            f' book={book}, page={page}')
