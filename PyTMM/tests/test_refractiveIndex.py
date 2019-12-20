import os
from unittest import TestCase

from PyTMM.refractiveIndex import RefractiveIndex

# DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                        os.path.normpath("../RefractiveIndex/"))


class TestRefractiveIndex(TestCase):

    def test_defaultInit(self):

        try:
            database = RefractiveIndex()
        except FileNotFoundError:
            print("database not found at default location, checking custom location from \'./refractiveindex_database_location.txt\'")
            database_path = ""
            with open("refractiveindex_database_location.txt", "r") as f:
                database_path = f.readline()

            database = RefractiveIndex(databasePath=database_path)
        else:
            assert os.path.exists(database.referencePath)
            assert os.path.exists(os.path.join(database.referencePath, os.path.normpath("library.yml")))
            assert os.path.isfile(os.path.join(database.referencePath, os.path.normpath("library.yml")))

        finally:
            assert os.path.exists(database.referencePath)
            assert os.path.exists(os.path.join(database.referencePath, os.path.normpath("library.yml")))
            assert os.path.isfile(os.path.join(database.referencePath, os.path.normpath("library.yml")))


    def test_getMaterialFilename(self):
        try:
            database = RefractiveIndex()
        except FileNotFoundError:
            print("database not found at default location, checking custom location from \'./refractiveindex_database_location.txt\'")
            database_path = ""
            with open("refractiveindex_database_location.txt", "r") as f:
                database_path = f.readline()

            database = RefractiveIndex(databasePath=database_path)

        for sh in database.catalog:
            for b in sh['content']:
                if 'DIVIDER' not in b:
                    for p in b['content']:
                        if 'DIVIDER' not in p:
                            mat = database.getMaterialFilename(sh['SHELF'], b['BOOK'], p['PAGE'])
                            assert os.path.exists(os.path.normpath(mat))
                            assert os.path.isfile(os.path.normpath(mat))

    def test_getMaterial(self):
        try:
            database = RefractiveIndex()
        except FileNotFoundError:
            print("database not found at default location, checking custom location from \'./refractiveindex_database_location.txt\'")
            database_path = ""
            with open("refractiveindex_database_location.txt", "r") as f:
                database_path = f.readline()

            database = RefractiveIndex(databasePath=database_path)

        for sh in database.catalog:
            for b in sh['content']:
                if 'DIVIDER' not in b:
                    for p in b['content']:
                        if 'DIVIDER' not in p:
                            try:
                                matfile = database.getMaterialFilename(sh['SHELF'], b['BOOK'], p['PAGE'])
                                mat = database.getMaterial(sh['SHELF'], b['BOOK'], p['PAGE'])
                            except Exception as err:
                                print(matfile)
                                print(err)
                                raise err
