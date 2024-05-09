from abc import ABC, abstractmethod
from enum import Enum

# create an abstract bass class to define solver frameworks
class SolverFramework(ABC):
    @property
    @abstractmethod
    def RelaxationSchemes(self) -> Enum:
        pass
    @property
    @abstractmethod
    def Solvers(self) -> Enum:
        pass
    @property
    @abstractmethod
    def IntergridTransfers(self) -> Enum:
        pass
    @property
    @abstractmethod
    def supports_relaxation_weights (self) -> bool: # relaxation weights for smoothers
        pass
    @property
    @abstractmethod
    def supports_scaling_factors(self) -> bool: # scaling factors for coarse-grid correction
        pass
    @property
    @abstractmethod
    def arg_dict_key(self) -> dict:
        pass
    @abstractmethod
    def __init__(self, exec_path: str) -> None:
        """
        Initialize the solver framework with the path to the executable
        """
        pass
    @abstractmethod
    def evaluate(self, arg_dict: dict) -> dict:
        """
        input: dictionary containing the solver configuration. 
        example: {'l_max': 3, 
                'rlx_wt': [0.5, 0.6, 0.7], 
                'rlx_scheme': [0, 13, 14],
                  'solver': 2, 
                  'scaling_factor': 0.5}

        output: multi-dimensional fitness output. 
        example: 
        {'average_convergence': 1e-2, 
        'worst_convergence': 1e-1,
        'total_iterations': 10,
        'solve_time': 0.1,
        'coarsegrid_time': 0.02}
        """
        pass