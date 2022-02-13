# Linear Solver for simplex tableau method
This repository contains a simple implementation of a linear programming solver, in particular for the primal and dual simplex method in tableau form and the application of Gomory's cut in case of integer linear problems. It can be useful for hand written exercises, in order to see intermediate tableau and check the solution step by step.

# Functionality
The code in this repository can perform the following actions:
* Primal Simplex method in tableau form
* Dual Simplex method in tableau form
* Two-Phase method (not full available yet)
* Gomory's cut for integer linear problem (ILP)

# How to use

### Standard solver from command line

1. Starting from a linear programming problem (LP) like:



2. Convert the problem into the correspondent tableau as the following, making sure it contains the initial basis:

<center>

  | // | // | x1 | x2 | x3 | x4 |
  | -- | -- | -- | -- | -- | -- |
  | z= |  0 | -1 | -1 |  0 |  0 |
  | x3 | 24 |  6 |  4 |  1 |  0 |
  | x4 |  6 |  3 | -2 |  0 |  1 |

</center>

3. Create a txt file containing only the values in the tableau, for example *'tableau.txt'*:

```
0 -1 -1 0 0
24 6 4 1 0
6 3 -2 0 1
```

4. Run the script **solver.py**, passing the tableau file as parameter:

```console
py solver.py tableau.txt
```

5. Then the resulting output will looks like, showing all the intermediate steps and informations about the pivot operations made:

```python
START TABLEAU:        
[[ 0. -1. -1.  0.  0.]
 [24.  6.  4.  1.  0.]
 [ 6.  3. -2.  0.  1.]]

TABLEAU:
[[ 2.          0.         -1.66666667  0.          0.33333333]
 [12.          0.          8.          1.         -2.        ]
 [ 2.          1.         -0.66666667  0.          0.33333333]]

TABLEAU:
[[ 4.5         0.          0.          0.20833333 -0.08333333]
 [ 1.5         0.          1.          0.125      -0.25      ]
 [ 3.          1.          0.          0.08333333  0.16666667]]

TABLEAU:
[[ 6.    0.5   0.    0.25  0.  ]
 [ 6.    1.5   1.    0.25  0.  ]
 [18.    6.    0.    0.5   1.  ]]

The tableau has an optimal solution x =  [0, 6.0, 0, 18.0]
```

### Pyhton function inline

1. First import the numpy package and the **Model** object from the file *'model.py'*:

```python
import numpy as np
from model import Model
```

2. Using the above notation on how representing in tableau form an LP or ILP problem, create a numpy array for the tableau and pass it into the **Model** object. Moreover indicate the initial basic variables indexes in another numpy array (in the example x3 and x4 so [3, 4]).

```python
tableau = np.array([[0., -1., -1., 0., 0.],
                    [24., 6., 4., 1., 0.],
                    [6., 3., -2., 0., 1.]])
basic_var = np.array([3, 4])
model = Model(tableau, basic_var)
```

5. Use the **primal_simplex_method()** to solve the problem by the primal simplex method. Otherwise the **dual_simplex_method()** for the dual simplex method. To visualize the intermediate tableau and other useful information set the parameter *verbose* to the correspondent integer value.

```python
model.primal_simplex_method(verbose=2)
```

```python
model.dual_simplex_method(verbose=2)
```

Further informations about all the functionalities available here in the Wiki.