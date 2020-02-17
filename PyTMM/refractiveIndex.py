""" TODO: add proper wavelength unit documentation in docstrings
TODO: remove lambda expression assignments.
FIXME: This sucks. Seriously. For one data point we have to open two files,
    and read the whole catalog.
EVERY FRIKIN' TIME
"""
import os
import sys
from io import open
from pathlib import Path

import numpy
import scipy.interpolate
import yaml

from .material import Material

DATA_BASE_PATH = Path(__file__).parent.parent / "glass_database"


class RefractiveIndex:
    """Class that parses the refractiveindex.info YAML database
    """

    def __init__(self, data_base_path=DATA_BASE_PATH):
        """

        :param data_base_path:
        """
        self.data_base_path = Path(data_base_path)
        fname = self.data_base_path / "library.yml"
        with open(fname, "rt", encoding="utf-8") as f:
            self.catalog = yaml.safe_load(f)

        # TODO: Do i NEED namedtuples, or am i just wasting time?
        # Shelf = collections.namedtuple('Shelf', ['SHELF', 'name', 'books'])
        # Book = collections.namedtuple('Book', ['BOOK', 'name', 'pages'])
        # Page = collections.namedtuple('Page', ['PAGE', 'name', 'path'])

        # self.catalog = [Shelf(**shelf) for shelf in rawCatalog]
        # for shelf in self.catalog:
        #     books = []
        #     for book in shelf.books:
        #         rawBook = book
        #         if not 'divider' in rawBook:
        #             books.append(Book(**rawBook))
        #         pages = []
        #         for page in book.pages:
        #             rawPage = page
        #             pages.append(Page(**rawPage))
        #         book.pages = pages

    # def get_material_filename(self, shelf, book, page):
    #     """

    #     ## Args:
    #         shelf
    #         book
    #         page
    #     :return:
    #     """
    #     filename = ''
    #     # FIXME:There MUST be a way to access an elements w/o iterating over the whole damn dictionary.
    #     for sh in self.catalog:
    #         if sh['SHELF'] == shelf:
    #             for b in sh['content']:
    #                 if 'DIVIDER' not in b:
    #                     if b['BOOK'] == book:
    #                         for p in b['content']:
    #                             if 'DIVIDER' not in p:
    #                                 if p['PAGE'] == page:
    #                                     # print("From {0} opening {1}, {2}\n".format(sh['name'], b['name'], p['name']))
    #                                     filename = os.path.join(
    #                                         self.data_base_path, 'data', os.path.normpath(p['data']))
    #                                     # print("Located at {}".format(filename))
    #     assert filename != ''
    #     return filename

    def get_material_filename(self, shelf, book, page):
        glass_catalog = book
        filename = page + '.yml'
        for root, _, files in os.walk(self.data_base_path):
            if root.endswith(glass_catalog):
                break
        for f in files:
            if f == filename:
                filepath = self.data_base_path / root / filename
                return filepath
        print(filepath)

    def get_material(self, shelf, book, page):
        """

        :param shelf:
        :param book:
        :param page:
        :return:
        """
        return Material(self.get_material_filename(shelf, book, page))


