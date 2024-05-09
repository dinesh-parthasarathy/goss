from .solver_framework import SolverFramework
from enum import Enum
import subprocess, re
# create a class for the mg framework hypre 
class Hypre(SolverFramework):
    class RelaxationSchemes(Enum):
        JACOBI = 0
        GS_FORWARD = 13
        GS_BACKWARD = 14
        GS_SYMMETRIC = 15
        CHEBYSHEV = 16
        L1_JACOBI = 17
        L1_GS_FORWARD = 19
        L1_GS_BACKWARD = 20
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
    supports_scaling_factors = True
    arg_dict_key = {'cycle_struct': [], 'rlx_schemes': [],'rlx_wts': [],'scaling_factors': []}
    def __init__(self, exec_path: str) -> None:
        self.exec_path = exec_path
    def evaluate(self, arg_dict: dict) -> dict:
        n_nodes = len(arg_dict['rlx_schemes'])
        arg_str = f"{n_nodes}/"
        arg_str += ",".join([str(x) for x in arg_dict['cycle_struct']]) + "/"
        arg_str += ",".join([str(x) for x in arg_dict['rlx_schemes']]) + "/"
        arg_str += ",".join([str(x) for x in arg_dict['rlx_wts']]) + "/"
        arg_str += ",".join(["1"]*n_nodes) + "/"
        arg_str += ",".join([str(x) for x in arg_dict['scaling_factors']])
        exec_args = [self.exec_path, "-amgusrinputs", "1", str(arg_str)]

        # run the code and pass the command line arguments from the input list
        output = subprocess.run(exec_args, capture_output=True, text=True)

        # check if the code ran successfully
        if output.returncode != 0:
            output = subprocess.run(exec_args, capture_output=True, text=True)
            print("error")
            #print(output.args)

        # parse the output to extract wall clock time, number of iterations, convergence factor. 
        output_lines = output.stdout.split('\n')
        run_time = [1e100] * 1
        n_iterations =[1e100] * 1
        convergence_factor = [1e100] * 1
        solve_phase = False
        i = 0 
        pattern = r"Cycle\s+\d+\s+([\d.e+-]+)\s+"
        residuals = []
        for line in output_lines:
            if "Cycle" in line:
                match = re.search(pattern, line)
                if match:
                    residuals.append(float(match.group(1)))
            if "Solve phase times" in line:
                solve_phase=True
            elif "wall clock time" in line and solve_phase:
                match = re.search(r'\d+\.\d+', line)
                if match:
                    run_time[i]=float(match.group())*1000 # convert to milliseconds
                solve_phase=False
            elif "Iterations" in line:
                match = re.search(r'\d+', line)
                if match:
                    n_iterations[i] = int(match.group())
                # from the list of residuals, calculate the convergence factor
                if len(residuals) > 4:
                    initial_residual = residuals[4]
                    final_residual = residuals[-1]
                    convergence_factor[i] = pow(final_residual/initial_residual, 1/(len(residuals)-4))
                elif len(residuals) > 1:
                    convergence_factor[i] = residuals[-2]/residuals[-1]
                residuals.clear()
                i += 1

        return {'convergence_factor': convergence_factor[0],
                'n_iterations': n_iterations[0],
                'run_time': run_time[0]}