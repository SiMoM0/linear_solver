# Linear Solver for simplex tableau method
This repository contains a simple implementation of a linear programming solver, in particular for the primal and dual simplex method in tableau form and the application of Gomory's cut in case of integer linear problems. It can be useful for hand written exercises, in order to see intermediate tableau and check the solution step by step.

# How to use
Starting from a linear programming problem (LP) like:

Convert the problem into the correspondent tableau as the following, making sure it contains the initial basis.

Create a numpy array for the tableau and pass it into the **Model** object.

Use the **primal_simplex_method()** to solve the problem by the primal simplex method. Otherwise the **dual_simplex_method()** for the dual simplex method.
