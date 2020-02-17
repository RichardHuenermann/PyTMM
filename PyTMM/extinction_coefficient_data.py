from scipy.interpolate import interp1d
import numpy as np


class ExtinctionCoefficientData:
    def __init__(self, wavelengths, coefficients):
        """constructor for a ExtinctionCoefficientData object.

        :param wavelengths:
        :param coefficients:
        """
        self.extCoeffFunction = interp1d(
            wavelengths, coefficients)
        self.rangeMin = np.min(wavelengths)
        self.rangeMax = np.max(wavelengths)

    def get_value(self, wavelength):
        """

        :param wavelength:
        :return: :raise Exception:
        """
        wavelength /= 1000.0
        if not self.rangeMin <= wavelength <= self.rangeMax:
            raise ValueError(
                f'Wavelength {wavelength} is out of bounds.'
                f' Correct range(um): ({self.rangeMin}, {self.rangeMax})')
        return self.extCoeffFunction(wavelength)


class NoExtinctionCoefficient(Exception):
    """Custom exception"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
