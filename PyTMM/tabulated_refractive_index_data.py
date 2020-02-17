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

    def get_refractive_index(self, wavelength):
        """

        Args:
            wavelength (float): in nm
        """
        wavelength /= 1000.0
        if self.rangeMin == self.rangeMax and self.rangeMin == wavelength:
            return self.refractiveFunction
        elif self.rangeMin <= wavelength <= self.rangeMax and self.rangeMin != self.rangeMax:
            return self.refractiveFunction(wavelength)
        else:
            raise ValueError(
                'Wavelength {} is out of bounds. Correct range(um): ({}, {})'.format(wavelength, self.rangeMin,
                                                                                     self.rangeMax))

