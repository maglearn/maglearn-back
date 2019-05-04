from enum import Enum


class Backend(Enum):
    PYTORCH = 1
    KERAS = 2
    MLP_C = 3
    MLP_CUDA = 4
