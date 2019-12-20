""" Defines TransferMatrix class.
TODO: try and make it possible to create multiple layers from numpy array of inputs.
"""

import enum

import numpy as np
from numpy import cos, exp, sin


class Polarization(enum.Enum):
    s = 0
    p = 1



class TransferMatrix:
    """
        Dielectric layer TMM

        How the functions eat structure matricies:

        | T |   |        | |        | |     |   | 1 |
        |   | = | Bottom | | Matrix | | Top | = |   |
        | 0 |   |        | |        | |     |   | R |

    """
    def __init__(self, matrix):
        self.matrix = matrix

    @classmethod
    def structure(cls, *args):
        """
        args - separate structure matricies
        Left to Right = Bottom to Top
        :param args:
        """
        mat = np.identity(2, dtype=np.complex128)
        for m in args:
            mat = np.dot(m.matrix, mat)
        return cls(mat)

    @classmethod
    def layer(cls, n, d, wavelength, theta=0, pol=Polarization.s):
        """
        Creates a Air-DielectricLayer-Air Transfer Matrix
        :param n:
        :param d:
        :param wavelength:
        """
        bottomBoundary = cls.boundingLayer(1, n, theta, pol)
        topBoundary = cls.boundingLayer(n, 1, theta, pol)
        propagation = cls.propagationLayer(
            n, d, wavelength, theta, pol)

        return cls.structure(bottomBoundary,
                             propagation,
                             topBoundary)

    @classmethod
    def boundingLayer(cls, n1, n2, theta=0, pol=Polarization.s):
        """
        Creates a DielectricLayer-DielectricLayer Boundary Transfer Matrix
        :param n1:
        :param n2:
        """
        # if np.abs((n1/n2)*sin(theta)) >= 1.0:
        #     theta2 = np.pi/2 * np.sign(sin(theta))
        # else:
        theta2 = np.arcsin((n1 / n2) * sin(theta),
                           dtype=np.complex128)

        # TE
        if pol is Polarization.s:
            _n1 = n1 * cos(theta)
            _n2 = n2 * cos(theta2)
            a21 = 1

        # TM
        elif pol is Polarization.p:
            _n1 = n1 / cos(theta)
            _n2 = n2 / cos(theta2)
            a21 = cos(theta2) / cos(theta)

        boundary = 1 / (2 * a21 * _n2) * np.array([[(_n1 + _n2), (_n2 - _n1)],
                                                   [(_n2 - _n1), (_n1 + _n2)]], dtype=np.complex128)
        return cls(boundary)

    @classmethod
    def propagationLayer(cls, n, d, wavelength, theta=0, pol=Polarization.s):
        """Creates a Propagation Transfer Matrix

        ## Args:
            n (float)  # refractive index
            d (float)  # width of layer
            wavelength (float)  # [nm]
        """
        theta2 = np.arcsin((1 / n) * sin(theta),
                           dtype=np.complex128)

        propagation = np.array([[exp((-1j * n * d * 2 * np.pi / wavelength) * cos(theta2)), 0],
                                [0, exp((1j * n * d * 2 * np.pi / wavelength) * cos(theta2))]],
                               dtype=np.complex128)
        return cls(propagation)


    def invert(self):
        """Inverts matrix
        """
        self.matrix = np.linalg.inv(self.matrix)

    def appendLeft(self, matrix):
        """append matrix to left of system

        ## Arg:
            matrix:
        """
        self.matrix = np.dot(matrix.matrix, self.matrix)

    def appendRight(self, matrix):
        """append matrix to right of system

        ## Arg:
            matrix:
        """
        self.matrix = np.dot(self.matrix, matrix.matrix)


    def solvePropagation(self, incidentField=1.0):
        """Calculate reflectance and transmittance
        ## Args:
            transferMatrix:
            incidentField:
        """
        # res[1] = transmittance, res[0] = reflectance
        lhs = np.array([[self.matrix[0, 1], -1],
                        [self.matrix[1, 1], 0]])
        rhs = np.array([- self.matrix[0, 0],
                        - self.matrix[1, 0]])
        rhs = np.multiply(rhs, incidentField)
        res = np.linalg.solve(lhs, rhs)
        reflectance = res[0]
        transmittance = res[1]
        return reflectance, transmittance


def findReciprocalTransferMatrix(transmittance, reflectance,
                                 bottomMat=TransferMatrix(np.identity(2)),
                                 topMat=TransferMatrix(np.identity(2))):  # , incidentField=1.0
    """find reciprocal transfer matrix.

    ## Args
        transmittance (complex)
        reflectance (complex)
        bottomMat (TransferMatrix, optional)  # defaults to unity matrix.
        topMat (TransferMatrix, optional)  # defaults to unity matrix.
    ## Returns
        TransferMatrix
    """
    assert transmittance != 0

    matrix = np.array([[1 / np.conj(transmittance), reflectance / transmittance],
                       [np.conj(reflectance / transmittance), 1 / transmittance]])
    matrix = np.dot(np.linalg.inv(bottomMat.matrix), matrix)
    matrix = np.dot(matrix, np.linalg.inv(topMat.matrix))
    return TransferMatrix(matrix)


def findReciprocalTransferMatrixLegacy(transmittance, reflectance,
                                       bottomMat=TransferMatrix(np.identity(2)),
                                       topMat=TransferMatrix(np.identity(2))):  # , incidentField=1.0
    """legacy version of find reciprocal transfer matrix method.

    ## Args
        transmittance (complex)
        reflectance (complex)
        bottomMat (TransferMatrix, optional)  # defaults to unity matrix.
        topMat (TransferMatrix, optional)  # defaults to unity matrix.
    ## Returns
        TransferMatrix
    """
    a = np.identity(2)
    b = np.array([[np.real(reflectance), np.imag(reflectance)],
                  [np.imag(reflectance), -np.real(reflectance)]])
    lhs = np.vstack((np.hstack((a, b)), np.hstack((b, a))))
    rhs = np.array([np.real(transmittance),
                    np.imag(transmittance), 0, 0])
    res = np.linalg.solve(lhs, rhs)
    matrix = np.array([[res[0] + 1j * res[1], res[2] - 1j * res[3]],
                       [res[2] + 1j * res[3], res[0] - 1j * res[1]]])

    matrix = np.dot(np.linalg.inv(bottomMat.matrix), matrix)
    matrix = np.dot(matrix, np.linalg.inv(topMat.matrix))
    return TransferMatrix(matrix)


def findGeneralizedTransferMatrix(transmitance1, reflectance1, transmitance2, reflectance2,
                                  bottomMat1=TransferMatrix(np.identity(2)),
                                  topMat1=TransferMatrix(np.identity(2)),
                                  bottomMat2=TransferMatrix(np.identity(2)),
                                  topMat2=TransferMatrix(np.identity(2))):
    """TODO: add docs

    ## Args:
        transmitance1 (complex)    #
        reflectance1 (complex)  #
        transmitance2 (complex)    #
        reflectance2 (complex)  #
        bottomMat1 (TransferMatrix, optional)  # defaults to unity matrix.
        topMat1 (TransferMatrix, optional)  # defaults to unity matrix.
        bottomMat2 (TransferMatrix, optional)  # defaults to unity matrix.
        topMat2 (TransferMatrix, optional)  # defaults to unity matrix.
    """
    a12 = np.dot(np.linalg.inv(bottomMat1.matrix),
                 np.array([[transmitance1], [0]]))
    a34 = np.dot(np.linalg.inv(bottomMat2.matrix),
                 np.array([[transmitance2], [0]]))

    b12 = np.dot(topMat1.matrix, np.array([[1], [reflectance1]]))
    b34 = np.dot(topMat2.matrix, np.array([[1], [reflectance2]]))

    rhs = np.array([a12[0, 0], a34[0, 0], a12[1, 0], a34[1, 0]])

    bmat = np.array([[b12[0, 0], b12[1, 0]],
                     [b34[0, 0], b34[1, 0]]])

    lhs = np.vstack((np.hstack((bmat, np.zeros((2, 2)))),
                     np.hstack((np.zeros((2, 2)), bmat))))
    res = np.linalg.solve(lhs, rhs)

    mat = np.array([[res[0], res[2]],
                    [res[1], res[3]]])
    return TransferMatrix(mat)
