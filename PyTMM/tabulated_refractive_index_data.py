import numpy as np
from scipy.interpolate import interp1d


class TabulatedRefractiveIndexData:
    """Tabulated RefractiveIndex class"""

    def __init__(self, wavelengths, values):
        """

        :param wavelengths:
        :param values:
        """
        self.rangeMin = np.min(wavelengths)
        self.rangeMax = np.max(wavelengths)

        if self.rangeMin == self.rangeMax:
            self.refractiveFunction = values[0]
        else:
            self.refractiveFunction = interp1d(wavelengths, values)

    def get_value(self, wavelength):
        """

        Args:
            wavelength (float): in nm
        """
        wavelength /= 1000.0
        if self.rangeMin == self.rangeMax and self.rangeMin == wavelength:
            return self.refractiveFunction
        elif all([self.rangeMin <= wavelength <= self.rangeMax,
                  self.rangeMin != self.rangeMax]):
            return self.refractiveFunction(wavelength)
        else:
            raise ValueError(
                f'Wavelength {wavelength} is out of bounds.'
                f' Correct range(um): ({self.rangeMin}, {self.rangeMax})')
