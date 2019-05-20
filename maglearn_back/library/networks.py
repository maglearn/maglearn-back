from enum import Enum
from typing import List


class NetworkType(Enum):
    MLP = 1
    RBF = 2


class MLPArchitecture(object):
    """Multilayer perceptron neural network architecture."""

    def __init__(self, input_size: int, hidden_sizes: List[int],
                 output_size: int):
        """Inits MLPArchitecture."""
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size


class RBFArchitecture(object):
    """Radial basis function neural network architecture."""
    pass


architectures = {
    NetworkType.MLP: MLPArchitecture,
    NetworkType.RDF: RBFArchitecture
}