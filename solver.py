#solve a linear programming problem
#run the code in the command line with a input txt file representing the problem
#example: py solver.py filename.txt integer
#where integer is 0 or 1 if the solution must be integer
import sys
import numpy as np
from solver.model import read_tableau

#check command line argument and print usage
if len(sys.argv) != 3:
    print('\nUSAGE: solver.py <filename.txt> <integer>')
    print('\nArguments:\n     <filename.txt>: path to the tableau file\n     <integer>: 1 if solution must be integer, 0 otherwise\n')
    sys.exit()

#get file name from command line
file = sys.argv[1]
integer = bool(sys.argv[2])

#create and solve the model
model = read_tableau(file, integer=integer)
model.solve(verbose=2)
model.print_solution()