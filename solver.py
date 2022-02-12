#solve a linear programming problem
#run the code in the command line with a input txt file representing the problem

from tabnanny import verbose
import numpy as np
from model import read_tableau

#file name
file = input('Insert the file name: ')

#create and solve the model
model = read_tableau(file)

model.primal_simplex_method(verbose=2)