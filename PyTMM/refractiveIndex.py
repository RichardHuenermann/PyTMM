""" TODO: add proper wavelength unit documentation in docstrings
TODO: remove lambda expression assignments.
FIXME: This sucks. Seriously. For one data point we have to open two files, and read the whole catalog.
EVERY FRIKIN' TIME
"""
import os
import yaml
import sys
import argparse
import numpy
import scipy.interpolate
from io import open

from .material import Material


class RefractiveIndex:
    """Class that parses the refractiveindex.info YAML database"""

    def __init__(self, databasePath=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 os.path.normpath("../RefractiveIndex/"))):
        """

        :param databasePath:
        """
        self.referencePath = os.path.normpath(databasePath)
        fileName = os.path.join(
            self.referencePath, os.path.normpath("library.yml"))
        with open(fileName, "rt", encoding="utf-8") as f:
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

    def get_material_filename(self, shelf, book, page):
        """

        :param shelf:
        :param book:
        :param page:
        :return:
        """
        filename = ''
        # FIXME:There MUST be a way to access an elements w/o iterating over the whole damn dictionary.
        for sh in self.catalog:
            if sh['SHELF'] == shelf:
                for b in sh['content']:
                    if 'DIVIDER' not in b:
                        if b['BOOK'] == book:
                            for p in b['content']:
                                if 'DIVIDER' not in p:
                                    if p['PAGE'] == page:
                                        # print("From {0} opening {1}, {2}\n".format(sh['name'], b['name'], p['name']))
                                        filename = os.path.join(
                                            self.referencePath, 'data', os.path.normpath(p['data']))
                                        # print("Located at {}".format(filename))
        assert filename != ''
        return filename

    def get_material(self, shelf, book, page):
        """

        :param shelf:
        :param book:
        :param page:
        :return:
        """
        return Material(self.get_material_filename(shelf, book, page))


# Stuff to link to matlab
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns refractive index of material for specified wavelength")
    parser.add_argument('catalog')
    parser.add_argument('section')
    parser.add_argument('book')
    parser.add_argument('page')
    parser.add_argument('wavelength')

    args = parser.parse_args()
    catalog = RefractiveIndex(args.catalog)
    mat = catalog.get_material(args.section, args.book, args.page)
    sys.stdout.write(str(mat.get_refractive_index(float(args.wavelength))))
