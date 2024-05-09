from __future__ import annotations
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './external/GeneticEngine')))
from geml.simplegp import SimpleGP
from geneticengine.grammar.utils import is_terminal
from goss.evaluator.hypre import Hypre  
global evaluator
import copy
def compile(p, arg_dict):

    type_name = type(p).__name__
    terminal = is_terminal(type(p), g.non_terminals)
    if not terminal:
        if "prolongate_and_cgc" in type_name or "restrict" in type_name:
            if "prolongate_and_cgc" in type_name:
                arg_dict['scaling_factors'].insert(0, p.iwt.value)
                arg_dict['cycle_struct'].insert(0, evaluator.IntergridTransfers.PROLONGATE.value)
            else:
                arg_dict['cycle_struct'].insert(0, evaluator.IntergridTransfers.RESTRICT.value)
                arg_dict['scaling_factors'].insert(0, 1)
            if len(arg_dict['cycle_struct']) > len(arg_dict['rlx_schemes']):
                arg_dict['rlx_schemes'].insert(0, evaluator.RelaxationSchemes.NO_SMOOTHING.value)
                arg_dict['rlx_wts'].insert(0, 1)
        elif "smooth" in type_name or "solve" in type_name:
            if "smooth" in type_name:
                arg_dict['rlx_wts'].insert(0, p.iwt.value)
                arg_dict['rlx_schemes'].insert(0, p.ischeme.value)
            else:
                arg_dict['rlx_schemes'].insert(0, p.isolver.value)
                arg_dict['rlx_wts'].insert(0, 1)
            if len(arg_dict['rlx_schemes']) > (len(arg_dict['cycle_struct']) + 1):
                arg_dict['cycle_struct'].insert(0, evaluator.IntergridTransfers.SAME_LEVEL.value)
                arg_dict['scaling_factors'].insert(0, 1) 
        return compile(p.previous_state, arg_dict)  
    else:
        if len(arg_dict['cycle_struct']) >= len(arg_dict['rlx_schemes']):
                arg_dict['rlx_schemes'].insert(0, evaluator.RelaxationSchemes.NO_SMOOTHING.value)
                arg_dict['rlx_wts'].insert(0, 1)
        elif len(arg_dict['rlx_schemes']) > (len(arg_dict['cycle_struct']) + 1):
            arg_dict['cycle_struct'].insert(0, evaluator.IntergridTransfers.SAME_LEVEL.value)
            arg_dict['scaling_factors'].insert(0, 1)
        assert ( len(arg_dict['cycle_struct']) + 1 ) == len(arg_dict['rlx_schemes']) == len(arg_dict['rlx_wts']) == (len(arg_dict['scaling_factors']) + 1)
        return arg_dict
def fitness_function(individual):
    arg_dict = compile(individual, copy.deepcopy(evaluator.arg_dict_key))
    fitness_dict = evaluator.evaluate(arg_dict)
    return fitness_dict['convergence_factor']
if __name__ == "__main__":
    
    # choose the evaluator/application.
    evaluator = Hypre(exec_path="/Users/dinesh/Documents/code/hypre/src/test/ij")

    # choose components from the application for optimization.
    irlxschemes = [evaluator.RelaxationSchemes.JACOBI.value, evaluator.RelaxationSchemes.GS_FORWARD.value, 
                  evaluator.RelaxationSchemes.GS_BACKWARD.value, evaluator.RelaxationSchemes.NO_SMOOTHING.value]
    isolvers = [evaluator.Solvers.GE.value]
    iscaling_factors = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0] if evaluator.supports_scaling_factors else [1]
    irlx_wts = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5] if evaluator.supports_relaxation_weights else [1]
    min_level = 0
    max_level = 4

    # choose a grammar description
    from goss.grammar.mg_arbitrarycycle import create_cfg 

    # extract grammar with the mg components chosen.
    g = create_cfg(min_level, max_level, irlxschemes, isolvers, irlx_wts, iscaling_factors)
    print("Grammar: {}.".format(repr(g)))

    # optimize using GP
    alg = SimpleGP(
    grammar=g,
    minimize=True,
    fitness_function=fitness_function,
    crossover_probability=0.75,
    mutation_probability=0.01,
    max_evaluations=10000,
    max_depth=10,
    population_size=50,
    selection_method=("tournament", 2),
    elitism=5
    )
    best = alg.search()
    print(
        f"Fitness of {best.get_fitness(alg.get_problem())} by genotype: {best.genotype} with phenotype: {best.get_phenotype()}",
    )

