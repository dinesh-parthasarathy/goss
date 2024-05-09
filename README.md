# GOSS
**G**rammar-guided **O**ptimisation for **S**ystem **S**imulations


## Installation
Clone the git repository via:

``` bash
git clone --recurse-submodules https://github.com/dinesh-parthasarathy/goss.git
```

## Setting up an optimization (with an exemplary test case)

### 1. Choose an evaluator/application ([List of evaluators](https://github.com/dinesh-parthasarathy/goss/tree/master/goss/evaluator))
```python
evaluator = Hypre(exec_path="/Users/dinesh/Documents/code/hypre/src/test/ij")
```
### 2. Choose components from the application for optimization ([List of components in hypre](https://github.com/dinesh-parthasarathy/goss/tree/master/goss/evaluator/hypre.py))
```python
irlxschemes = [evaluator.RelaxationSchemes.JACOBI.value, evaluator.RelaxationSchemes.GS_FORWARD.value, 
                evaluator.RelaxationSchemes.GS_BACKWARD.value, evaluator.RelaxationSchemes.NO_SMOOTHING.value]
isolvers = [evaluator.Solvers.GE.value]
iscaling_factors = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0] if evaluator.supports_scaling_factors else [1]
irlx_wts = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5] if evaluator.supports_relaxation_weights else [1]
min_level = 0
max_level = 4
```
### 3. Choose a grammar description ([List of grammars](https://github.com/dinesh-parthasarathy/goss/tree/master/goss/grammar))
```python
from goss.grammar.mg_arbitrarycycle import create_cfg 
```
### 4. Extract grammar with the components chosen
```python
g = create_cfg(min_level, max_level, irlxschemes, isolvers, irlx_wts, iscaling_factors)
```
### 5. Optimize using GP (List of [representations](https://geneticengine.readthedocs.io/en/latest/representations.html)/ [algorithms](https://geneticengine.readthedocs.io/en/latest/algorithms.html))
```python
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
```
