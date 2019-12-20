import argparse
import os
import sys
from io import open

import scipy.interpolate
import yaml

from . import (ExtinctionCoefficientData, FormulaRefractiveIndexData,
               RefractiveIndex, TabulatedRefractiveIndexData)


class Material:
    """ Material class"""

    def __init__(self, filename):
        """constructor for Material object.

        ## Args:
            filename:
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

                    self.refractiveIndex = TabulatedRefractiveIndexData(wavelengths=wavelengths,
                                                                        values=n)
                elif (data['type'].split())[1] == 'k':
                    self.extinctionCoefficient = ExtinctionCoefficientData.setup_extinction_coefficient(
                        wavelengths, n)

                elif (data['type'].split())[1] == 'nk':
                    if self.refractiveIndex is not None:
                        Exception('Bad Material YAML File')

                    self.refractiveIndex = TabulatedRefractiveIndexData(wavelengths=wavelengths,
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

                self.refractiveIndex = FormulaRefractiveIndexData(formula=formula,
                                                                  rangeMin=rangeMin,
                                                                  rangeMax=rangeMax,
                                                                  coefficients=coefficents)

    def get_refractive_index(self, wavelength):
        """returns refractive index

        Args:
            wavelength (float)  # in nm
        """
        if self.refractiveIndex is None:
            raise Exception('No refractive index specified for this material')
        else:
            return self.refractiveIndex.get_refractive_index(wavelength)

    def get_extinction_coefficient(self, wavelength):
        """Returns extinction coefficient

        Args:
            wavelength (float)  # [nm]
        """
        if self.extinctionCoefficient is None:
            raise ValueError(
                'No extinction coefficient specified for this material')
        else:
            return self.extinctionCoefficient.get_extinction_coefficient(wavelength)
