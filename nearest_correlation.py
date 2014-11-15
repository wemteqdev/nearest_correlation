import numpy as np
from numpy import diag, inf
from numpy import copy, dot
from numpy.linalg import norm


class NotSymmetric(Exception):
    pass


class NotImplemented(Exception):
    pass


class ExceededMaxIterations(Exception):
    def __init__(self, msg, matrix=[], iteration=[], dS=[]):
        self.msg = msg
        self.matrix = copy(matrix)
        self.iteration = iteration
        self.dS = copy(dS)

    def __str__(self):
        return repr(self.msg)


def nearcorr(A, tol=[], flag=0, maxiterations=100, n_pos_eig=0,
             weights=np.array([]), verbose=False, dS=np.array([])):
    """
    X = nearcorr(A, tol=[], flag=0, maxiterations=100, n_pos_eig=0,
        weights=np.array([]),print=0)

    Finds the nearest correlation matrix to the symmetric matrix A.

    ARGUMENTS
    ~~~~~~~~~
    tol is a convergence tolerance, which defaults to 16*EPS.
    If using flag == 1, tol must be a size 2 tuple, with first component
    the convergence tolerance and second component a tolerance
    for defining "sufficiently positive" eigenvalues.

    flag = 0: solve using full eigendecomposition (EIG).
    flag = 1: treat as "highly non-positive definite A" and solve
    using partial eigendecomposition (EIGS). CURRENTLY NOT IMPLEMENTED

    maxiterations is the maximum number of iterations (default 100,
    but may need to be increased).

    n_pos_eig (optional) is the known number of positive eigenvalues
    of A. CURRENTLY NOT IMPLEMENTED

    weights is a vector defining a diagonal weight matrix diag(W).

    verbose = True for display of intermediate output.
    CURRENTLY NOT IMPLEMENTED

    dS is the starting value for the variable dS thats used in the main loop.
    Useful when restarting from a calculation where maxiterations
    has been exceeded

    ABOUT
    ~~~~~~
    This is a Python port by Michael Croucher, November 2014

    Original MATLAB code by N. J. Higham, 13/6/01, updated 30/1/13.
    Reference:  N. J. Higham, Computing the nearest correlation
    matrix---A problem from finance. IMA J. Numer. Anal.,
    22(3):329-343, 2002.
    """
    eps = np.spacing(1)
    if not np.all((np.transpose(A) == A)):
        raise NotSymmetric('Input Matrix is not symmetric')
    if not tol:
        tol = eps * np.shape(A)[0] * np.array([1, 1])
    if weights.size == 0:
        weights = np.ones((np.shape(A)[0], 1))
    X = copy(A)
    Y = copy(A)
    rel_diffY = inf
    rel_diffX = inf
    rel_diffXY = inf
    if dS.size == 0:
        dS = np.zeros(np.shape(A))

    Whalf = np.sqrt(np.outer(weights, weights))

    iteration = 0
    while max(rel_diffX, rel_diffY, rel_diffXY) > tol[0]:
        iteration += 1
        if iteration > maxiterations:
            if maxiterations == 1:
                message = "No solution found in "\
                          + str(maxiterations) + " iteration"
            else:
                message = "No solution found in "\
                          + str(maxiterations) + " iterations"
            raise ExceededMaxIterations(message, X, iteration, dS)

        Xold = copy(X)
        R = X - dS
        R_wtd = Whalf*R
        if flag == 0:
            X = proj_spd(R_wtd)
        elif flag == 1:
            raise NotImplemented("Setting 'flag' to 1 is currently\
                                 not implemented.")
        X = X / Whalf
        dS = X - R
        Yold = copy(Y)
        Y = copy(X)
        np.fill_diagonal(Y, 1)
        normY = norm(Y, 'fro')
        rel_diffX = norm(X - Xold, 'fro') / norm(X, 'fro')
        rel_diffY = norm(Y - Yold, 'fro') / normY
        rel_diffXY = norm(Y - X, 'fro') / normY

        X = copy(Y)

    return X, iteration


def proj_spd(A):
    d, v = np.linalg.eigh(A)
    A = v.dot(diag(nonneg(d))).dot(v.conj().T)
    A = (A + A.conj().T) / 2
    return(A)


def nonneg(A):
    B = copy(A)
    B[B < 0] = 0
    return(B)
