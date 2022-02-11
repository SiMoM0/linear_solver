# Linear Solver for simplex tableau method
This repository contains a simple implementation of a linear programming solver, in particular for the primal and dual simplex method in tableau form and the application of Gomory's cut in case of integer linear problems. It can be useful for hand written exercises, in order to see intermediate tableau and check the solution step by step.

# How to use
Starting from a linear programming problem (LP) like:

Convert the problem into the correspondent tableau as the following, making sure it contains the initial basis.

  |    |    | x1 | x2 | x3 | x4 |
  | -- | -- | -- | -- | -- | -- |
  | z= |  0 | -1 | -1 |  0 |  0 |
  | x3 | 24 |  6 |  4 |  1 |  0 |
  | x4 |  6 |  3 | -2 |  0 |  1 |

Create a numpy array for the tableau and pass it into the **Model** object.

```python
tableau = np.array([[0., -1., -1., 0., 0.], [24., 6., 4., 1., 0.], [6., 3., -2., 0., 1.]])
model = Model(tableau)
```

Use the **primal_simplex_method()** to solve the problem by the primal simplex method. Otherwise the **dual_simplex_method()** for the dual simplex method.

```python
model.primal_simplex_method()
```
