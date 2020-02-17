"""Python library for TMM and RefractiveIndex.info database operations
"""
from .extinctionCoefficientData import (ExtinctionCoefficientData,
                                        NoExtinctionCoefficient)
from .formulaRefractiveIndexData import FormulaRefractiveIndexData
from .material import Material
from .material_library import DATA_BASE_PATH, MaterialLibrary
from .tabulatedRefractiveIndexData import TabulatedRefractiveIndexData
from .transferMatrix import Polarization, TransferMatrix

__all__ = [
    'FormulaRefractiveIndexData',
    'ExtinctionCoefficientData',
    'MaterialLibrary',
    'ExtinctionCoefficientData',
    'NoExtinctionCoefficient',
    'TabulatedRefractiveIndexData',
    'Material',
    'TransferMatrix',
    'Polarization']

__author__ = "Pavel Dmitriev"
__version__ = "1.0.2"
__license__ = "GPLv3"
