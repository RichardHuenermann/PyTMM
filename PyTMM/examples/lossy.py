"""Calculates reflectivity of lossy materials
"""
import matplotlib.pyplot as plt
import numpy as np

from PyTMM.transferMatrix import TransferMatrix


wavelengths = np.linspace(300, 1500, 2000)
r = np.zeros(wavelengths.shape)
r1 = np.zeros(wavelengths.shape)
r2 = np.zeros(wavelengths.shape)
r3 = np.zeros(wavelengths.shape)


for i, lam in enumerate(wavelengths):
    a = TransferMatrix.layer(1.46, 200, lam)
    b = TransferMatrix.layer(1.46 - 0.001j, 200, lam)
    c = TransferMatrix.layer(1.46 - 0.01j, 200, lam)
    d = TransferMatrix.layer(1.46 - 0.1j, 200, lam)

    R, _ = a.solvePropagation()
    r[i] = (np.abs(R) ** 2)
    R, _ = b.solvePropagation()
    r1[i] = (np.abs(R) ** 2)
    R, _ = c.solvePropagation()
    r2[i] = (np.abs(R) ** 2)
    R, _ = d.solvePropagation()
    r3[i] = (np.abs(R) ** 2)

plt.title('Reflectance of a lossy material')
plt.plot(wavelengths, r, label='1.46')
plt.plot(wavelengths, r1, label='1.46-0.001j')
plt.plot(wavelengths, r2, label='1.46-0.01j')
plt.plot(wavelengths, r3, label='1.46-0.1j')
plt.xlabel('wavelength (nm)')
plt.ylabel('reflectance')
plt.legend(loc='best')
plt.show()
