"""Python library for TMM and RefractiveIndex.info database operations
"""
from .extinction_coefficient_data import (ExtinctionCoefficientData,
                                          NoExtinctionCoefficient)
from .formula_refractive_index_data import FormulaRefractiveIndexData
from .material import Material
from .material_library import DATA_BASE_PATH, MaterialLibrary
from .tabulated_refractive_index_data import TabulatedRefractiveIndexData
from .transfer_matrix import Polarization, TransferMatrix

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
