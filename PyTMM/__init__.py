"""Python library for TMM and RefractiveIndex.info database operations
"""
from .extinctionCoefficientData import (ExtinctionCoefficientData,
                                        NoExtinctionCoefficient)
from .formulaRefractiveIndexData import FormulaRefractiveIndexData
from .material import Material
from .refractiveIndex import RefractiveIndex
from .tabulatedRefractiveIndexData import TabulatedRefractiveIndexData
from .transferMatrix import Polarization, TransferMatrix

__all__ = [
    'FormulaRefractiveIndexData',
    'ExtinctionCoefficientData',
    'RefractiveIndex',
    'ExtinctionCoefficientData',
    'NoExtinctionCoefficient',
    'TabulatedRefractiveIndexData',
    'Material',
    'TransferMatrix',
    'Polarization']

__author__ = "Pavel Dmitriev"
__version__ = "1.0.2"
__license__ = "GPLv3"
