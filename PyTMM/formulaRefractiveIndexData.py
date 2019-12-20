import numpy as np


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
        return np.sqrt(nsq)

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
        return np.sqrt(nsq)

    def ntype_polynomial(self, wavelength):

        def g(c1, c2, w):
            return c1 * w**c2

        nsq = self.coefficients[0]
        for i in range(1, len(self.coefficients), 2):
            nsq += g(self.coefficients[i],
                     self.coefficients[i + 1], wavelength)
        return np.sqrt(nsq)

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
        return np.sqrt(nsq)

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

