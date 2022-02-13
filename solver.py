#solve a linear programming problem
#run the code in the command line with a input txt file representing the problem
#example: py solver.py filename.txt
import sys
import numpy as np
from model import read_tableau

#get file name from command line
file = sys.argv[1]

#create and solve the model
model = read_tableau(file)
model.primal_simplex_method(verbose=2)