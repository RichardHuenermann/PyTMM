import os
from unittest import TestCase
import pytest

from PyTMM import MaterialLibrary, Material

# DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                        os.path.normpath("../RefractiveIndex/"))


class TestMaterialLibrary(TestCase):
    def setUp(self):
        self.library = MaterialLibrary()

    def test_default_init(self):
        db_path = self.library.data_path
        lib_yml = db_path.parent / "library.yml"
        assert lib_yml.is_file()

    def test_get_material_file(self):
        """iterates over entire library.yml and makes sure all files are found.
        TODO: this doesn't succeed and I dont know why.
        """
        for shelf in self.library.catalog:
            for book in shelf['content']:
                if 'DIVIDER' in book:
                    continue
                for page in book['content']:
                    if 'DIVIDER' in page:
                        continue
                    mat_file = self.library.get_material_file(
                        shelf['SHELF'], book['BOOK'], page['PAGE'])
                    assert mat_file.is_file()


    def test_get_fname_nonexistent(self):
        """This file has the problem that the filename is not contained in the
        library.yml.

        The individual files are named

            Lemarchand-11.7nm.yml
            Lemarchand-3.96nm.yml
            Lemarchand-4.62nm.yml
            Lemarchand-5.77nm.yml
        and have the same page, book and catalog.

        """
        material_library = MaterialLibrary()
        shelf = 'main'
        book = 'Au'
        page = 'Lemarchand-doesntexist'
        with pytest.raises(FileNotFoundError):
            material_library.get_material_file(
                shelf=shelf, book=book, page=page)

