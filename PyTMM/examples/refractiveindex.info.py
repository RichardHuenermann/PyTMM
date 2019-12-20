import numpy
import matplotlib.pyplot as plt
import os

from PyTMM.transferMatrix import TransferMatrix
from PyTMM.refractiveIndex import RefractiveIndex

database = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        os.path.normpath("../../../refractiveindex.info-database/database/"))
catalog = RefractiveIndex(database)

sio2 = catalog.get_material('main', 'SiO2', 'Malitson')

ran = range(400, 800, 1)
reflectance = []

for i in ran:
    a = TransferMatrix.boundingLayer(1, sio2.get_refractive_index(i))
    R, T = a.solvePropagation()
    reflectance.append(numpy.abs(R ** 2))

plt.plot(ran, reflectance)
plt.xlabel("wavelength, nm")
plt.ylabel("reflectance")
plt.title("Reflectance of single SiO2 Boundary")
plt.show(block=True)