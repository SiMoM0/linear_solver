#Example for the primal simplex method in tableau form
#Tableau used:
#           x1  x2  x3  x4
#   z=   0  -1  -1   0   0
#   x3  24   6   4   1   0
#   x4   6   3  -2   0   1

import numpy as np
from model import Model

#PRIMAL SIMPLEX METHOD TEST
tableau = np.array([[0., -1., -1., 0., 0.],
                    [24., 6., 4., 1., 0.],
                    [6., 3., -2., 0., 1.]])
basic_var = np.array([1, 2])

model = Model(tableau, basic_var)

model.primal_simplex_method(verbose=True)