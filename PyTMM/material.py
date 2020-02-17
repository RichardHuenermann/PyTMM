import argparse
import os
import sys
from io import open

import scipy.interpolate
import yaml

from .formula_refractive_index_data import FormulaRefractiveIndexData
from .extinction_coefficient_data import ExtinctionCoefficientData
from .tabulated_refractive_index_data import TabulatedRefractiveIndexData
from .material_library import MaterialLibrary


class Material:
    """ Material class"""

    def __init__(self, filename):
        """constructor for Material object.

        ## Args:
            filename:
        """
        self.data_path = filename
        self.refractive_index = None
        self.extinction_coefficient = None

        with open(filename, "rt", encoding="utf-8") as f:
            material = yaml.safe_load(f)

        for data in material['DATA']:
            data_type = (data['type'].split())[0]
            if data_type == 'tabulated':
                self.read_tabulated_data(data)
            elif data_type == 'formula':
                self.read_formula_data(data)

    def read_formula_data(self, data: dict):
        if self.refractive_index is not None:
            Exception('Bad Material YAML File')

        formula = int((data['type'].split())[1])
        coefficents = [float(s) for s in data['coefficients'].split()]
        for k in ['range', 'wavelength_range']:
            if k in data:
                break
        rangeMin = float(data[k].split()[0])
        rangeMax = float(data[k].split()[1])

        self.refractive_index = FormulaRefractiveIndexData(
            formula, rangeMin, rangeMax, coefficents)

    def read_tabulated_data(self, data: dict):
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

        if 'n' in (data['type'].split())[1]:
            if self.refractive_index is not None:
                Exception('Bad Material YAML File')
            self.refractive_index = TabulatedRefractiveIndexData(
                wavelengths=wavelengths, values=n)

        elif (data['type'].split())[1] == 'k':
            self.extinction_coefficient = ExtinctionCoefficientData(
                wavelengths, n)

        if (data['type'].split())[1] == 'nk':
            self.extinction_coefficient = ExtinctionCoefficientData(
                wavelengths, k)

    @classmethod
    def from_catalog(cls, material_library, shelf, book, page):
        """replaces the ugly method MaterialLibrary.get_material()
        """
        catalog_path = material_library.get_material_file(shelf, book, page)
        return cls(catalog_path)

    def get_refractive_index(self, wavelength):
        """returns refractive index

        Args:
            wavelength (float)  # in nm
        """
        if self.refractive_index is None:
            raise AttributeError(
                'No refractive index specified for this material')
        else:
            return self.refractive_index.get_value(wavelength)

    def get_extinction_coefficient(self, wavelength):
        """Returns extinction coefficient

        Args:
            wavelength (float)  # [nm]
        """
        if self.extinction_coefficient is None:
            raise AttributeError(
                'No extinction coefficient specified for this material')
        else:
            return self.extinction_coefficient.get_value(wavelength)
