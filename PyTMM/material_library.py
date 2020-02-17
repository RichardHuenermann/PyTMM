import os
import sys
from io import open
from pathlib import Path

import numpy
import scipy.interpolate
import yaml


DATA_BASE_PATH = Path(__file__).parent.parent / "glass_database"


class MaterialLibrary:
    """Class that parses the refractiveindex.info YAML database
    TODO: rename to MaterialLibrary
    """

    def __init__(self, data_base_path=DATA_BASE_PATH):
        """

        :param data_base_path:
        """
        self.path = Path(data_base_path)
        fname = self.path / "library.yml"
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

        for book_iter in shelf_iter['content']:
            try:
                if book_iter['BOOK'] == book:
                    break
            except KeyError:
                continue

        for page_iter in book_iter['content']:
            if 'DIVIDER' in page_iter:
                continue
            if page_iter['PAGE'] == page:
                return self.path / page_iter['path']
        raise FileNotFoundError(
            f'Material file not found with parameters: shelf={shelf},'
            f' book={book}, page={page}')

    def _get_material_file_opticspy(self, shelf, book, page):
        """returns path to file corresponding to arguments
        This method is weird and iterates over the filenames
        instead of the yaml file.
        dont use this..

        previous name: get_material_filename

        Args:
            shelf (str): [description]
            book (str): [description]
            page (str): [description]

        Returns:
            path (Path): path to yml file containing material info.
        """
        glass_catalog = book
        my_fname = page + '.yml'
        for root, _, files in os.walk(self.path):
            if root.endswith(glass_catalog):
                break

        contains_name = []
        for file in files:
            if file == my_fname:
                filepath = self.path / root / my_fname
                if filepath.exists():
                    return filepath
            if page in file:
                contains_name.append(file)
        contains_msg = ""
        for file in contains_name:
            contains_msg += f"\nDid you mean {file}?"
        raise FileNotFoundError(
            f'The file {my_fname} could not be found.' + contains_msg)




    # def get_material(self, shelf, book, page):
    #     """  this is really ugly and unnecessary.
    #     TODO: Should be put into Material class as classmethod.

    #     :param shelf:
    #     :param book:
    #     :param page:
    #     :return:
    #     """
    #     catalog_path = self.get_material_file(shelf, book, page)
    #     return Material(catalog_path)

