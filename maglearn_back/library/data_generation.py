import abc
from typing import Tuple

import numpy as np


class Function(abc.ABC):
    """Encapsulates data generation functions."""

    def __init__(self, name, input_size, output_size):
        """Inits Function."""
        self.name = name
        self.input_size = input_size
        self.output_size = output_size

    @abc.abstractmethod
    def __call__(self, x):
        """Calculate function value."""
        pass

    @property
    @abc.abstractmethod
    def latex_repr(self):
        """Presents latex representation of the function which can be rendered
        in GUI."""
        pass


class DampedSineWave(Function):
    """Damped sine wave function."""

    def __init__(self, a=1, lambda_=0.1, omega=1, phi=0):
        """Inits DampedSineWave."""
        Function.__init__(self, "Damped Sine Wave", 1, 1)
        self._a = a
        self._lambda = lambda_
        self._omega = omega
        self._phi = phi

    def __call__(self, x):
        return (self._a
                * np.exp(-1 * self._lambda * x)
                * np.cos(self._omega * x + self._phi))

    @property
    def latex_repr(self):
        r = f"""y(x) = A \\cdot e^{{-\\lambda x}} \\cdot cos(\\omega x + \\phi)
        \\\\ A = {self._a}
        \\\\ \\lambda = {self._lambda}
        \\\\ \\omega = {self._omega}
        \\\\ \\phi = {self._phi}"""
        return r


functions = [DampedSineWave]


def generate_random_fun_samples(fun: Function, samples: int,
                                *ranges: Tuple[float, float],
                                noise: bool = True):
    """Generates random function samples in given ranges."""
    xs = [np.random.uniform(lo, hi, samples).T for lo, hi in ranges]
    X = np.column_stack(xs)
    Y = fun(X)
    mask = np.isfinite(Y).ravel()
    X = X[mask]
    Y = Y[mask]
    if noise:
        Y += np.random.random_sample(Y.shape) / 20
    return X, Y
