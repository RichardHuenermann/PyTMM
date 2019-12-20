"""Calculates angle dependent reflectance for special case of total internal reflection.
"""

import numpy as np
import matplotlib.pyplot as plt

from PyTMM.transferMatrix import TransferMatrix, Polarization

n = 2
angles_of_incidence = np.linspace(0, np.pi / 2, 1000)
reflection_TE_polarization = []
reflection_TM_polarization = []
for aoi in angles_of_incidence:
    # TE
    a = TransferMatrix.boundingLayer(n, 1, aoi, Polarization.s)

    R, T = a.solvePropagation()
    reflection_TE_polarization.append(np.abs(R**2))

    # TM
    a = TransferMatrix.boundingLayer(n, 1, aoi, Polarization.p)
    R, T = a.solvePropagation()
    reflection_TM_polarization.append(np.abs(R**2))


plt.plot(angles_of_incidence, reflection_TE_polarization)
plt.plot(angles_of_incidence, reflection_TM_polarization)
plt.xlabel("Angle, rad")
plt.ylabel("Reflectance")
plt.title("Angle dependence of reflectivity")
plt.legend(['TE', 'TM'], loc='best')
plt.show(block=True)
