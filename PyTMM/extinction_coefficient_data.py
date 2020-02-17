from scipy.interpolate import interp1d
import numpy as np


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
        self.extCoeffFunction = interp1d(
            wavelengths, coefficients)
        self.rangeMin = np.min(wavelengths)
        self.rangeMax = np.max(wavelengths)

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
                f'Wavelength {wavelength} is out of bounds.'
                f' Correct range(um): ({self.rangeMin}, {self.rangeMax})')


class NoExtinctionCoefficient(Exception):
    """Custom exception"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
