import matplotlib.pyplot as plt
import numpy

from PyTMM import DATA_BASE_PATH, MaterialLibrary, TransferMatrix, Material

library = MaterialLibrary()
sio2 = Material.from_catalog(library, 'main', 'SiO2', 'Malitson')

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
