'''
not implemented yet
'''
"""
--------grammar description for multigrid solvers with V-cycle-like structures---------------
<S> ::= <s_lmax>
<s_lmax> ::=  SMOOTH(l_max, <rlx_wt>, <rlx_scheme>, <s_lmax>) | CGC(l_max, <scaling_factor>, <sup_lmax-1> | u_0
<sup_l> ::= SMOOTH(l, <rlx_wt>, <rlx_scheme>, <sup_l>) | CGC(l, <scaling_factor>, <sup_l-1>  
<sdown_l> ::= SMOOTH(l, <rlx_wt>, <rlx_scheme>, <sdown_l>) | SMOOTH(l, <rlx_wt>, <rlx_scheme>, <sdown_l+1>) | SOLVE(l, <solver>, <sdown_l+1>)
<s_0> ::= SOLVE(l, <solver>, <sdown_1>)
<rlx_wt> ::= 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0
<scaling_factor> ::= 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0
<rlx_scheme> ::= Jacobi | GS | ... |
<solver> ::= GE | CG | ... |
"""