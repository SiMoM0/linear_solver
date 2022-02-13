#example for an ILP problem using first primal simplex, then a combination of gomory cuts and dual simplex method
import numpy as np
from model import Model

tableau = np.array([[0, -4, -5, 0, 0, 0],
                    [8, 2, 2, 1, 0, 0],
                    [7, 1, 3, 0, 1, 0],
                    [5, 2, 1, 0, 0, 1]], dtype='float')
beta = [3, 4, 5]

model = Model(tableau=tableau, basic_var=beta, integer=True)
model.solve(verbose= 2)
model.print_solution()

#with the following tableau there is a problem about fraction number, which does not stop the algorithm
'''
tableau3 = np.array([[0, -3, -2, 0, 0, 0], [7, 2, 1, 1, 0, 0], [8, 3, 2, 0, 1, 0], [6, 1, 1, 0, 0, 1]], dtype='float')
beta3 = [3, 4, 5]
model = Model(tableau=tableau3, basic_var=beta3, integer=True)
model.solve(verbose= 2)
model.print_solution()
'''