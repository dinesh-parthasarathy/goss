'''
not implemented yet
'''

from solver_framework import SolverFramework
from enum import Enum

# create a class for the mg framework hypre 
class Hyteg(SolverFramework):
    class RelaxationSchemes(Enum):
        JACOBI = 0
        GS_FORWARD = 13
        GS_BACKWARD = 14
        CHEBYSHEV = 16
        UZAWA = 17
        NO_SMOOTHING = -1
    class Solvers(Enum):
        CG = 2
        GMRES = 1
        GE = 9
    class IntergridTransfers(Enum):
        RESTRICT = -1
        PROLONGATE = 1
        SAME_LEVEL = 0
    supports_relaxation_weights = True 
    supports_scaling_factors = False
    def evaluate(self, arg_dict: dict) -> dict:
        pass