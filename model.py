#package required
import numpy as np

#parameters: tableau, index t of the row, index h of the column
def pivot_operation(tableau, t, h):
    #shape of the tableau
    m = tableau.shape[0]
    n = tableau.shape[1]
    pivot = tableau[t][h]
    #divide the pivot row by the pivot element
    for i in range(n):
        tableau[t][i] /= pivot
    #update all the other rows
    save = pivot
    for i in range(m):
        if i != t and tableau[i][h] != 0:
            save = tableau[i][h]
            for j in range(n):
                tableau[i][j] -= save*tableau[t][j]

class Model():
    """
	Implement the linear programming problem in tableau form
	Each object has two attributes:
		-The tableau on which perform operations
		-The list of initial basic variables
	"""

    def __init__(self, tableau, basic_var):
        self.tableau = tableau
        self.basic_var = basic_var

    def primal_simplex_method(self, two_phase=False, verbose=False):
        tableau = self.tableau
        beta = self.basic_var
        #print the starting tableau
        print('START TABLEAU:\n{}\n'.format(tableau))

        #number of rows in the tableau
        m = tableau.shape[0]
        #number of columns in the tableau
        n = tableau.shape[1]

        #final cases
        unbounded = False
        optimal = False

        while optimal == False and unbounded == False:
            #get the vector of costs
            costs = [tableau[0][c] for c in range(1, n)]
            #verify if all the costs are >= 0, thus the tableau is in optimal form
            if all(c >= 0 for c in costs):
                optimal = True
                break
            else:
                #index of the non basic variable
                h = 0
                #Find the first cost < 0 and choose a non basic variable
                for i, c in enumerate(tableau[0]):
                    if i != 0 and c < 0:
                        h = i
                        #print('Variable of index {} will enter the basis'.format(h))
                        break
                #check if all the a[i, h] are < 0 so the problem is unbounded
                if all(tableau[i, h] < 0 for i in range(m)):
                    unbounded = True
                    break
                else:
                    #choose the variable that will leave the basis
                    min = 100000
                    t = 1
                    for i in range(1, m):
                        if tableau[i][h] > 0 and tableau[i][0] / tableau[i][h] < min:
                            min = tableau[i][0] / tableau[i][h]
                            t = i
                    #print('Pivot operation on the cell: {}\n'.format((t, h)))

                    #pivot operation
                    pivot_operation(tableau, t, h)

                    #update the vector beta, containing the indices of the basis variables
                    beta[t-1] = h

            #Print the intermediate tableau
            if verbose:
                print('TABLEAU:\n{}\n'.format(tableau))

        #solution
        x = [0]*(n - 1)
        for i, b in enumerate(beta):
            x[b-1] = tableau[i+1][0]

        if two_phase:
            return tableau, beta

        if optimal:
            print('The tableau has an optimal solution x = ', x)
        elif unbounded:
            print('The tableau is unbounded')        