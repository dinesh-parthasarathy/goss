
"""
--------grammar description for multigrid solvers with arbitrary cycles ---------------

<S> ::= <s_lmax>
<s_lmax> ::=  SMOOTH(l_max, <rlx_wt>, <rlx_scheme>, <s_lmax>) | CGC(l_max, <scaling_factor>, <s_lmax-1> | u_0
<s_lsolved> ::= SOLVE(l, <solver>, <s_l>)
<s_l> ::= SMOOTH(l, <rlx_wt>, <rlx_scheme>, <s_l>) | CGC(l, <scaling_factor>, <s_l-1> | CGC(l, <scaling_factor>, <s_lsolved-1> |SMOOTH(l, <rlx_wt>, <rlx_scheme>, <s_l+1>) | RESTRICT(l,  <s_l+1>)
<s_0solved> ::= SOLVE(l, <solver>, <s_0>) 
<s_0> ::= RESTRICT(l, <s_1>)
<rlx_wt> ::= 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0
<scaling_factor> ::= 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0
<rlx_scheme> ::= Jacobi | GS | ... |
<solver> ::= GE | CG | ... |
"""

from abc import ABC
from dataclasses import dataclass
from geneticengine.grammar.grammar import extract_grammar
from typing import Annotated
from geneticengine.grammar.metahandlers.ints import IntList
from geneticengine.grammar.metahandlers.floats import FloatList


def create_cfg(min_level, max_level, irlxschemes, isolvers, irlx_wts, iscaling_factors):
    # I. Create abstract classes to store data types
    state = {}
    state_solved = {}
    # 1. mg components
    class rlx_scheme(ABC):
        pass
    class solver(ABC):
        pass
    class rlx_wt(ABC):
        pass
    class scaling_factor(ABC):
        pass
    # 2. mg levels
    for i in range(min_level, max_level+1):
        state[i] = type(f'state_l{i}', (ABC,), {'__module__': '__main__'}) 
        state_solved[i] =  type(f'state_l{i}solved', (ABC,), {'__module__': '__main__'})       
    # II. create terminals
    class u_0(state[max_level]):
       lvl: int = int(max_level)
       pass
    @dataclass
    class rlxscheme_val(rlx_scheme):
        value: Annotated[int, IntList(irlxschemes)]
        pass
    @dataclass
    class solver_val(solver):
        value: Annotated[int, IntList(isolvers)]
        pass
    @dataclass
    class rlxwtval(rlx_wt):
        value: Annotated[float, FloatList(irlx_wts)]
        pass
    @dataclass
    class scalingfactor_val(scaling_factor):
        value : Annotated[float, FloatList(iscaling_factors)]
        pass

    # III. create non-terminals / productions
    non_terminals = []
    for i in range(min_level, max_level+1):
        if i == min_level:
            non_terminals.append(dataclass(type(f'solve_l{i}', 
                                        (state_solved[i],), 
                                        {'isolver': None, 'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'isolver': solver_val, 
                                                              'previous_state': state[i]}})))
            non_terminals.append(dataclass(type(f'restrict_l{i+1}', 
                                        (state[i],), 
                                        {'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'previous_state': state[i+1]}})))
        elif i == max_level:
            non_terminals.append(dataclass(type(f'smooth_l{i}', 
                                        (state[i],), 
                                        {'iwt': None, 'ischeme': None, 'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'iwt': rlxwtval, 
                                                              'ischeme': rlxscheme_val, 
                                                              'previous_state': state[i]}})))
            non_terminals.append(dataclass(type(f'prolongate_and_cgc_l{i}', 
                                        (state[i],), 
                                        {'iwt': None, 'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'iwt': scalingfactor_val, 
                                                              'previous_state': state[i-1]}})))
            non_terminals.append(dataclass(type(f'prolongate_and_cgc_l{i}', 
                                        (state[i],), 
                                            {'iwt': None, 'previous_state': None, 'lvl': i,
                                             '__module__': '__main__',
                                             '__annotations__': {'iwt': scalingfactor_val, 
                                                                 'previous_state': state_solved[i-1]}})))
        elif i == min_level + 1:
            non_terminals.append(dataclass(type(f'restrict_l{i+1}', 
                                        (state[i],), 
                                        {'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'previous_state': state[i+1]}})))
            non_terminals.append(dataclass(type(f'smooth_l{i}', 
                                        (state[i],), 
                                        {'iwt': None, 'ischeme': None, 'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'iwt': rlxwtval, 
                                                              'ischeme': rlxscheme_val, 
                                                              'previous_state': state[i]}})))
            non_terminals.append(dataclass(type(f'prolongate_and_cgc_l{i}', 
                                        (state[i],), 
                                        {'iwt': None, 'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'iwt': scalingfactor_val, 
                                                              'previous_state': state_solved[i-1]}})))
            non_terminals.append(dataclass(type(f'solve_l{i}', 
                                        (state_solved[i],), 
                                        {'isolver': None, 'previous_state': None, 'lvl': i,
                                          '__module__': '__main__',
                                          '__annotations__': {'isolver': solver_val, 
                                                              'previous_state': state[i]}})))
            
        else:
            non_terminals.append(dataclass(type(f'restrict_l{i+1}', 
                                        (state[i],), 
                                        {'previous_state': None, 'lvl': i,
                                         '__module__': '__main__',
                                         '__annotations__': {'previous_state': state[i+1]}})))
            non_terminals.append(dataclass(type(f'smooth_l{i}', 
                                        (state[i],), 
                                        {'iwt': None, 'ischeme': None, 'previous_state': None, 'lvl': i,
                                         '__module__': '__main__',
                                         '__annotations__': {'iwt': rlxwtval, 
                                                             'ischeme': rlxscheme_val, 
                                                             'previous_state': state[i]}})))
            non_terminals.append(dataclass(type(f'prolongate_and_cgc_l{i}', 
                                        (state[i],), 
                                        {'iwt': None, 'previous_state': None, 'lvl': i,
                                         '__module__': '__main__',
                                         '__annotations__': {'iwt': scalingfactor_val, 
                                                             'previous_state': state[i-1]}})))
            non_terminals.append(dataclass(type(f'prolongate_and_cgc_l{i}', 
                                        (state[i],), 
                                        {'iwt': None, 'previous_state': None, 'lvl': i,
                                         '__module__': '__main__',
                                         '__annotations__': {'iwt': scalingfactor_val, 
                                                             'previous_state': state_solved[i-1]}})))
            non_terminals.append(dataclass(type(f'solve_l{i}', 
                                        (state_solved[i],), 
                                        {'isolver': None, 'previous_state': None, 'lvl': i,
                                         '__module__': '__main__',
                                         '__annotations__': {'isolver': solver_val, 
                                                             'previous_state': state[i]}})))

    g = extract_grammar([u_0, rlxscheme_val, rlxwtval, solver_val, scalingfactor_val] # terminals
                        + non_terminals, # non-terminals
                         state[max_level]) 
    return g