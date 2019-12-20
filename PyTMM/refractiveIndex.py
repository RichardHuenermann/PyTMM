""" TODO: add proper wavelength unit documentation in docstrings
TODO: remove lambda expression assignments.
"""
import os
import yaml
import sys
import argparse
import numpy
import scipy.interpolate
from io import open


# import collections


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

    def getMaterialFilename(self, shelf, book, page):
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

    def getMaterial(self, shelf, book, page):
        """

        :param shelf:
        :param book:
        :param page:
        :return:
        """
        return Material(self.getMaterialFilename(shelf, book, page))


class Material:
    """ Material class"""

    def __init__(self, filename):
        """

        :param filename:
        """
        self.refractiveIndex = None
        self.extinctionCoefficient = None

        with open(filename, "rt", encoding="utf-8") as f:
            material = yaml.safe_load(f)

        for data in material['DATA']:
            if (data['type'].split())[0] == 'tabulated':
                rows = data['data'].split('\n')
                splitrows = [c.split() for c in rows]
                wavelengths = []
                n = []
                k = []
                for s in splitrows:
                    if len(s) > 0:
                        wavelengths.append(float(s[0]))
                        n.append(float(s[1]))
                        if len(s) > 2:
                            k.append(float(s[2]))

                if (data['type'].split())[1] == 'n':

                    if self.refractiveIndex is not None:
                        Exception('Bad Material YAML File')

                    self.refractiveIndex = RefractiveIndexData.setup_refractive_index(formula=-1,
                                                                                      wavelengths=wavelengths,
                                                                                      values=n)
                elif (data['type'].split())[1] == 'k':
                    self.extinctionCoefficient = ExtinctionCoefficientData.setup_extinction_coefficient(
                        wavelengths, n)

                elif (data['type'].split())[1] == 'nk':
                    if self.refractiveIndex is not None:
                        Exception('Bad Material YAML File')

                    self.refractiveIndex = RefractiveIndexData.setup_refractive_index(formula=-1,
                                                                                      wavelengths=wavelengths,
                                                                                      values=n)
                    self.extinctionCoefficient = ExtinctionCoefficientData.setup_extinction_coefficient(
                        wavelengths, k)
            elif (data['type'].split())[0] == 'formula':

                if self.refractiveIndex is not None:
                    Exception('Bad Material YAML File')

                formula = int((data['type'].split())[1])
                coefficents = [float(s) for s in data['coefficients'].split()]
                for k in ['range', 'wavelength_range']:
                    if k in data:
                        break
                rangeMin = float(data[k].split()[0])
                rangeMax = float(data[k].split()[1])

                self.refractiveIndex = RefractiveIndexData.setup_refractive_index(formula=formula,
                                                                                  rangeMin=rangeMin,
                                                                                  rangeMax=rangeMax,
                                                                                  coefficients=coefficents)

    def get_refractive_index(self, wavelength):
        """

        :param wavelength:
        :return: :raise Exception:
        """
        if self.refractiveIndex is None:
            raise Exception('No refractive index specified for this material')
        else:
            return self.refractiveIndex.get_refractive_index(wavelength)

    def get_extinction_coefficient(self, wavelength):
        """

        :param wavelength:
        :return: :raise NoExtinctionCoefficient:
        """
        if self.extinctionCoefficient is None:
            raise NoExtinctionCoefficient(
                'No extinction coefficient specified for this material')
        else:
            return self.extinctionCoefficient.get_extinction_coefficient(wavelength)


#
# Refractive Index
#
class RefractiveIndexData:
    """Abstract RefractiveIndex class"""

    @staticmethod
    def setup_refractive_index(formula, **kwargs):
        """

        :param formula:
        :param kwargs:
        :return: :raise Exception:
        """
        if formula >= 0:
            return FormulaRefractiveIndexData(formula, **kwargs)
        elif formula == -1:
            return TabulatedRefractiveIndexData(**kwargs)
        else:
            raise KeyError('Bad RefractiveIndex data type: {}'.format(formula))

    def get_refractive_index(self, wavelength):
        """

        :param wavelength:
        :raise NotImplementedError:
        """
        raise NotImplementedError(
            'Different for functionally and experimentally defined materials')


class FormulaRefractiveIndexData:
    """Formula RefractiveIndex class"""

    def __init__(self, formula, rangeMin, rangeMax, coefficients):
        """constructor for FormulaRefractiveIndexData object

            formula (int)  # selector for which refractive index formula will be used.
            rangeMin (float)  # minimum wavelength in microns.
            rangeMax (float)  # maximum wavelength in microns
            coefficients (list)  # list of floats, coefficients
        """
        assert formula in range(
            0, 7), 'Formula {} is not a valid option.'.format(formula)
        self.formula = formula
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self.coefficients = coefficients

    def get_ri_formula_name(self):
        """Returns name of the selected refractive index formula given by self.formula.
        """
        ntype_dict = {1: 'sellmeier1',
                      2: 'sellmeier2',
                      3: 'polynomial',
                      4: 'refindexinfo',
                      5: 'cauchy',
                      6: 'gasses',
                      7: 'herzberger',
                      8: 'retro',
                      9: 'exotic'}
        return ntype_dict[self.formula]

    def get_refractive_index(self, wavelength):
        """selects refractive index method and returns the value at the speciffied wavelength.

        Args:
            wavelength (float): in nanometers.

        Raises:
            ValueError: if wavelength out of bounds
            KeyError: if self.formula is wrong.
        """
        wavelength /= 1000.0
        if not (self.rangeMin <= wavelength <= self.rangeMax):
            raise ValueError(
                'Wavelength {}um is out of bounds. Correct range(um): ({}, {})'.format(wavelength,
                                                                                       self.rangeMin,
                                                                                       self.rangeMax))
        ntype_switch = {1: self.ntype_sellmeier1,
                        2: self.ntype_sellmeier2,
                        3: self.ntype_polynomial,
                        4: self.ntype_refindexinfo,
                        5: self.ntype_cauchy,
                        6: self.ntype_gasses,
                        7: self.ntype_herzberger,
                        8: self.ntype_retro,
                        9: self.ntype_exotic}
        if self.formula not in ntype_switch:
            raise KeyError(
                'formula type {} does not exist.'.format(self.formula))
        return ntype_switch[self.formula](wavelength)

    def ntype_sellmeier1(self, wavelength):
        """Sellmeier equation
        """
        nsq = 1 + self.coefficients[0]

        def sellmeier1_helper(c1, c2, w):
            return c1 * (w**2) / (w**2 - c2**2)

        for i in range(1, len(self.coefficients), 2):
            # TODO: make loop pythonic (list expression?)
            nsq += sellmeier1_helper(self.coefficients[i],
                                     self.coefficients[i + 1], wavelength)
        return numpy.sqrt(nsq)

    def ntype_sellmeier2(self, wavelength):
        """Sellmeier equation
        TODO: make loop pythonic (list expression?)
        """
        nsq = 1 + self.coefficients[0]

        def sellmeier2_helper(c1, c2, w):
            return c1 * (w**2) / (w**2 - c2)

        for i in range(1, len(self.coefficients), 2):
            # TODO: make loop pythonic (list expression?)
            nsq += sellmeier2_helper(self.coefficients[i],
                                     self.coefficients[i + 1], wavelength)
        return numpy.sqrt(nsq)

    def ntype_polynomial(self, wavelength):

        def g(c1, c2, w):
            return c1 * w**c2

        nsq = self.coefficients[0]
        for i in range(1, len(self.coefficients), 2):
            nsq += g(self.coefficients[i],
                     self.coefficients[i + 1], wavelength)
        return numpy.sqrt(nsq)

    def ntype_refindexinfo(self, wavelength):
        def g1(c1, c2, c3, c4, w):
            return c1 * w**c2 / (w**2 - c3**c4)

        def g2(c1, c2, w):
            return c1 * w**c2

        nsq = self.coefficients[0]
        for i in range(1, min(8, len(self.coefficients)), 4):
            nsq += g1(self.coefficients[i], self.coefficients[i + 1],
                      self.coefficients[i + 2], self.coefficients[i + 3], wavelength)
        if len(self.coefficients) > 9:
            for i in range(9, len(self.coefficients), 2):
                nsq += g2(self.coefficients[i],
                          self.coefficients[i + 1], wavelength)
        return numpy.sqrt(nsq)

    def ntype_cauchy(self, wavelength):
        def cauchy_helper(c1, c2, w):
            return c1 * w**c2

        ref_index = self.coefficients[0]
        for i in range(1, len(self.coefficients), 2):
            ref_index += cauchy_helper(self.coefficients[i],
                                       self.coefficients[i + 1], wavelength)
        return ref_index

    def ntype_gasses(self, wavelength):
        def gasses_helper(c1, c2, w):
            return c1 / (c2 - w**(-2))

        ref_index = 1 + self.coefficients[0]
        for i in range(1, len(self.coefficients), 2):
            ref_index += gasses_helper(self.coefficients[i],
                                       self.coefficients[i + 1], wavelength)
        return ref_index

    def ntype_herzberger(self, wavelength):
        def g1(c1, w, p):
            return c1 / (w**2 - 0.028)**p

        def g2(c1, w, p):
            return c1 * w**p

        ref_index = self.coefficients[0]
        ref_index += g1(self.coefficients[1], wavelength, 1)
        ref_index += g1(self.coefficients[2], wavelength, 2)
        for i in range(3, len(self.coefficients)):
            ref_index += g2(self.coefficients[i], wavelength, 2 * (i - 2))
        return ref_index

    def ntype_retro(self, wavelength):
        raise NotImplementedError(
            'refractive index formula not implemented yet.')

    def ntype_exotic(self, wavelength):
        raise NotImplementedError(
            'refractive index formula not implemented yet.')


class TabulatedRefractiveIndexData:
    """Tabulated RefractiveIndex class"""

    def __init__(self, wavelengths, values):
        """

        :param wavelengths:
        :param values:
        """
        self.rangeMin = numpy.min(wavelengths)
        self.rangeMax = numpy.max(wavelengths)

        if self.rangeMin == self.rangeMax:
            self.refractiveFunction = values[0]
        else:
            self.refractiveFunction = scipy.interpolate.interp1d(
                wavelengths, values)

    def get_refractive_index(self, wavelength):
        """

        :param wavelength:
        :return: :raise Exception:
        """
        wavelength /= 1000.0
        if self.rangeMin == self.rangeMax and self.rangeMin == wavelength:
            return self.refractiveFunction
        elif self.rangeMin <= wavelength <= self.rangeMax and self.rangeMin != self.rangeMax:
            return self.refractiveFunction(wavelength)
        else:
            raise Exception(
                'Wavelength {} is out of bounds. Correct range(um): ({}, {})'.format(wavelength, self.rangeMin,
                                                                                     self.rangeMax))


class ExtinctionCoefficientData:
    """ExtinctionCofficient class"""

    @staticmethod
    def setup_extinction_coefficient(wavelengths, values):
        """

        :param wavelengths:
        :param values:
        :return:
        """
        return ExtinctionCoefficientData(wavelengths, values)

    def __init__(self, wavelengths, coefficients):
        """

        :param wavelengths:
        :param coefficients:
        """
        self.extCoeffFunction = scipy.interpolate.interp1d(
            wavelengths, coefficients)
        self.rangeMin = numpy.min(wavelengths)
        self.rangeMax = numpy.max(wavelengths)

    def get_extinction_coefficient(self, wavelength):
        """

        :param wavelength:
        :return: :raise Exception:
        """
        wavelength /= 1000.0
        if self.rangeMin <= wavelength <= self.rangeMax:
            return self.extCoeffFunction(wavelength)
        else:
            raise Exception(
                'Wavelength {} is out of bounds. Correct range(um): ({}, {})'.format(wavelength, self.rangeMin,
                                                                                     self.rangeMax))


class NoExtinctionCoefficient(Exception):
    """Custom exception"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Stuff to link to matlab
# FIXME: This sucks. Seriously. For one data point we have to open two files, and read the whole catalog.
# EVERY FRIKIN' TIME
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
    mat = catalog.getMaterial(args.section, args.book, args.page)
    sys.stdout.write(str(mat.get_refractive_index(float(args.wavelength))))
