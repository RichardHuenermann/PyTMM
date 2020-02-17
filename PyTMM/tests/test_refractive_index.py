import os
from unittest import TestCase
import pytest

from PyTMM import MaterialLibrary, Material

# DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                        os.path.normpath("../RefractiveIndex/"))


class TestMaterialLibrary(TestCase):
    def test_default_init(self):

        material_library = MaterialLibrary()
        db_path = material_library.path
        lib_yml = db_path / "library.yml"
        assert lib_yml.is_file()


    def test_get_material_file(self):
        """iterates over entiere library.yml and makes sure all files are found.
        """
        material_library = MaterialLibrary()

        for shelf in material_library.catalog:
            for book in shelf['content']:
                if 'DIVIDER' in book:
                    continue
                for page in book['content']:
                    if 'DIVIDER' in page:
                        continue
                    mat_file = material_library.get_material_file(
                        shelf['SHELF'], book['BOOK'], page['PAGE'])
                    assert mat_file.is_file()

    def test_get_material_file_old(self):
        """iterates over entiere library.yml and makes sure all files are found.
        """
        material_library = MaterialLibrary()

        for shelf in material_library.catalog:
            for book in shelf['content']:
                if 'DIVIDER' in book:
                    continue
                for page in book['content']:
                    if 'DIVIDER' in page:
                        continue
                    mat_file = material_library._get_material_file_opticspy(
                        shelf['SHELF'], book['BOOK'], page['PAGE'])
                    assert mat_file.is_file()

    def test_get_mat_file_hikari(self):
        material_library = MaterialLibrary()
        shelf = 'glass'
        book = 'HIKARI-FK'
        page = 'J-KF6'
        mat_file = material_library.get_material_file(shelf, book, page)
        assert mat_file.is_file()

    def test_get_fname_au_lemarchand(self):
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
        page = 'Lemarchand'
        with pytest.raises(FileNotFoundError):
            material_library.get_material_file(
                shelf=shelf, book=book, page=page)

