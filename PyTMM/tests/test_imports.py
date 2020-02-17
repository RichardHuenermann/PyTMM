"""This test imports everything in the module and makes sure no errors occur.
"""
from unittest import TestCase
from importlib import import_module

from PyTMM.refractiveIndex import RefractiveIndex


class TestImports(TestCase):
    def test_import_pytmm(self):
        import_module('PyTMM')
        assert True

    def test_import_material(self):
        import_module('PyTMM.material')

    def test_import_transfer_matrix(self):
        getattr(import_module('PyTMM'), 'TransferMatrix')
