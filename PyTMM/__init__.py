"""
Python library for TMM and RefractiveIndex.info database operations
"""
from .formulaRefractiveIndexData import FormulaRefractiveIndexData
from .extinctionCoefficientData import ExtinctionCoefficientData
from .extinctionCoefficientData import ExtinctionCoefficientData, NoExtinctionCoefficient
from .tabulatedRefractiveIndexData import TabulatedRefractiveIndexData
from .material import Material  # must be before RefractiveIndex.
from .refractiveIndex import RefractiveIndex

__all__ = [
    'FormulaRefractiveIndexData',
    'ExtinctionCoefficientData',
    'RefractiveIndex',
    'ExtinctionCoefficientData',
    'NoExtinctionCoefficient',
    'TabulatedRefractiveIndexData',
    'Material']

__author__ = "Pavel Dmitriev"
__version__ = "1.0.2"
__license__ = "GPLv3"
