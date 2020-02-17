"""This test imports everything in the module and makes sure no errors occur.
"""
from unittest import TestCase
from importlib import import_module


class TestImports(TestCase):
    def test_import_pytmm(self):
        import_module('PyTMM')
        assert True

    def test_import_classes(self):
        all_classes = [
            'FormulaRefractiveIndexData',
            'ExtinctionCoefficientData',
            'MaterialLibrary',
            'ExtinctionCoefficientData',
            'NoExtinctionCoefficient',
            'TabulatedRefractiveIndexData',
            'Material',
            'TransferMatrix',
            'Polarization']
        for my_class in all_classes:
            getattr(import_module('PyTMM'), my_class)
