import os
from unittest import TestCase

from PyTMM.refractiveIndex import RefractiveIndex

# DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                        os.path.normpath("../RefractiveIndex/"))


class TestRefractiveIndex(TestCase):

    def test_default_init(self):

        try:
            database = RefractiveIndex()
        except FileNotFoundError:
            print("database not found at default location, checking custom location from \'./refractiveindex_database_location.txt\'")
            data_base_path = ""
            with open("refractiveindex_database_location.txt", "r") as f:
                data_base_path = f.readline()

            database = RefractiveIndex(data_base_path=data_base_path)
        else:
            assert os.path.exists(database.data_base_path)
            assert os.path.exists(os.path.join(database.data_base_path, os.path.normpath("library.yml")))
            assert os.path.isfile(os.path.join(database.data_base_path, os.path.normpath("library.yml")))

        finally:
            assert os.path.exists(database.data_base_path)
            assert os.path.exists(os.path.join(database.data_base_path, os.path.normpath("library.yml")))
            assert os.path.isfile(os.path.join(database.data_base_path, os.path.normpath("library.yml")))


    def test_get_material_filename(self):
        database = RefractiveIndex()

        for sh in database.catalog:
            for b in sh['content']:
                if 'DIVIDER' not in b:
                    for p in b['content']:
                        if 'DIVIDER' not in p:
                            mat = database.get_material_filename(
                                sh['SHELF'], b['BOOK'], p['PAGE'])
                            assert os.path.exists(os.path.normpath(mat))
                            assert os.path.isfile(os.path.normpath(mat))

    def test_get_au_lemarchand_filename(self):
        database = RefractiveIndex()
        shelf = 'main'
        book = 'Au'
        page = 'Lemarchand'
        mat = database.get_material_filename(
            shelf=shelf, book=book, page=page)
        assert os.path.exists(os.path.normpath(mat))
        assert os.path.isfile(os.path.normpath(mat))

    def test_get_material(self):
        """if get_material_filename doesn't work, then get_material cannot work either.
        """
        database = RefractiveIndex()

        for sh in database.catalog:
            for b in sh['content']:
                if 'DIVIDER' not in b:
                    for p in b['content']:
                        if 'DIVIDER' not in p:
                            try:
                                matfile = database.get_material_filename(sh['SHELF'], b['BOOK'], p['PAGE'])
                                mat = database.get_material(sh['SHELF'], b['BOOK'], p['PAGE'])
                            except Exception as err:
                                print(matfile)
                                print(err)
                                raise err


if __name__ == '__main__':


    # manually testing get_material_filename
    try:
        database = RefractiveIndex()
    except FileNotFoundError:
        print("database not found at default location, checking custom location from \'./refractiveindex_database_location.txt\'")
        data_base_path = ""
        with open("refractiveindex_database_location.txt", "r") as f:
            data_base_path = f.readline()
        database = RefractiveIndex(data_base_path)

    for sh in database.catalog:
        print(sh)
        for b in sh['content']:
            if 'DIVIDER' in b:
                continue
            for p in b['content']:
                if 'DIVIDER' in p:
                    continue
                mat = database.get_material_filename(sh['SHELF'], b['BOOK'], p['PAGE'])
                assert os.path.exists(os.path.normpath(mat))
                assert os.path.isfile(os.path.normpath(mat))
