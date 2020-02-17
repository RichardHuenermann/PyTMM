import os
from unittest import TestCase
import pytest

from PyTMM import MaterialLibrary, Material


class TestMaterial(TestCase):
    def setUp(self):
        self.library = MaterialLibrary()

    def test_material_init(self):
        """iterates over entire library.yml and creates Material objects
        """
        for shelf in self.library.catalog:
            for book in shelf['content']:
                if 'DIVIDER' in book:
                    continue
                for page in book['content']:
                    if 'DIVIDER' in page:
                        continue
                    Material.from_catalog(
                        self.library, shelf['SHELF'], book['BOOK'], page['PAGE'])

    # TODO: test_get_refractive_index(self)
    # TODO: test_get_tabulated_refractive_index(self):
    # TODO: test_get_refractive_index_no_data(self):
    # TODO: test_get_refractive_index_formula1(self):
    # TODO: test_get_refractive_index_formula2(self):
    # TODO: test_get_refractive_index_formula3(self):
    # TODO: test_get_refractive_index_formula4(self):
    # TODO: test_get_refractive_index_formula5(self):
    # TODO: test_get_refractive_index_formula6(self):
    # TODO: test_get_refractive_index_formula7(self):
