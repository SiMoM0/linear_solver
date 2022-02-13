#package required
import numpy as np

class Model():
    """
	Implement the linear programming problem in tableau form.
	
    Parameters:
        - tableau: a numpy array representing the tableau on which perform operations
        - basic_var: a list of initial basic variables
        - integer: a boolean value indicating if the solution has to be integer

    Attributes:
        - start_tableau: the initial tableau passed as input
        - tableau: the current tableau
        - basic_var: a numpy array containing indexes of the current basic variables
        - integer: a boolean value indicating if the solution has to be integer
        - solution: an array representing the final solution if exists
        - z: the optimal value if exists
	"""

    def __init__(self, tableau, basic_var, integer=False):
        self.start_tableau = tableau
        self.tableau = tableau
        self.basic_var = basic_var
        self.integer = integer
        self.solution = []
        self.z = 0
        self.optimal = False
        self.unbounded = False
        self.infeasible = False

    def print_solution(self):
        if self.solution != None:
            print('The tableau has an optimal solution x = {}\nand the optimal value is z = {}'.format(self.solution, self.z))
        elif self.unbounded:
            print('The tableau is unbounded')
        elif self.infeasible:
            print('The tableau is infeasible')

    #parameters: tableau, index t of the row, index h of the column
    def pivot_operation(self, t, h):
        '''
        Performs the pivot operations of the cell represented by the input values for row t and column h
        '''
        tableau = self.tableau
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

    def gomory_cut(self, verbose=0):
        '''
        Apply gomory's cut on the first fractional basic variables and add a new basic variable into the tableau.
        '''
        tableau = self.tableau
        beta = self.basic_var

        #number of rows in the tableau
        m = tableau.shape[0]
        #number of columns in the tableau
        n = tableau.shape[1]

        #apply gomory cut on the first fractional variable (fract is the index)
        fract = 0
        for i in range(1, m):
            if tableau[i][0] != int(tableau[i][0]):
                fract = i
                break
        #print the tableau with the gomory cut
        if verbose:
            print('TABLEAU WITH GOMORY CUT ON ROW=', fract)
        #add the new row
        tableau = np.vstack((tableau, np.array([0.]*n)))
        #add the new column
        tableau = np.hstack((tableau, np.zeros((m+1, 1), dtype=float)))
        tableau[m][n] = 1.
        
        #update the order of the tableau and the vector beta
        m = tableau.shape[0]
        n = tableau.shape[1]
        beta.append(n-1)
        #update the value in the new row added
        for i in range(n-1):
            if tableau[fract][i] >= 0:
                tableau[m-1][i] = -(tableau[fract][i] - int(tableau[fract][i]))
            else:
                tableau[m-1][i] = -(tableau[fract][i] - int(tableau[fract][i]-1))
        if verbose:
            print(tableau)
            print('\n')

        #reassign tableau and basic_var
        self.tableau = tableau
        self.basic_var = beta

    def primal_simplex_method(self, two_phase=False, verbose=0):
        '''
        Solve the model using the primal simplex method in tableau form.
        Parameters:
            - verbose: integer value to obtain the followig informations
                - 1 print the intermediate tableau
                - 2 show the pivot operations made
        Returns:
            - final tableau
            - 
        '''
        tableau = self.tableau
        beta = self.basic_var
        #print the starting tableau
        if verbose:
            print('TABLEAU:\n{}\n'.format(tableau))

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

                    if verbose == 2:
                        print('Pivot operation on element {} in the cell: {}\n'.format(tableau[t][h], (t, h)))

                    #pivot operation
                    self.pivot_operation(t, h)

                    #update the vector beta, containing the indices of the basis variables
                    beta[t-1] = h

            #Print the intermediate tableau
            if verbose:
                print('TABLEAU:\n{}\n'.format(tableau))

        if two_phase:
            return tableau, beta

        if optimal:
            #solution
            x = [0]*(n - 1)
            for i, b in enumerate(beta):
                x[b-1] = tableau[i+1][0]
            self.optimal = True
            self.solution = x
            self.z = -tableau[0][0]
            #print('The tableau has an optimal solution x = ', x)
        elif unbounded:
            self.unbounded = True
            #print('The tableau is unbounded')    

    def dual_simplex_method(self, verbose=0):
        '''
        Solve the model using the dual simplex method in tableau form.
        Parameters:
            - verbose: integer value to obtain the followig informations
                - 1 print the intermediate tableau
                - 2 show the pivot operations made
        '''
        tableau = self.tableau
        beta = self.basic_var
        #print the starting tableau
        if verbose:
            print('TABLEAU:\n{}\n'.format(tableau))

        #number of rows in the tableau
        m = tableau.shape[0]
        #number of columns in the tableau
        n = tableau.shape[1]

        #final cases
        infeasible = False
        optimal = False

        while optimal == False and infeasible == False:
            #get the vector of costs
            b_vector = [tableau[b][0] for b in range(1, m)]
            #verify if all the costs are >= 0, thus the tableau is in optimal form
            if all(b >= 0 for b in b_vector):
                optimal = True
                break
            else:
                #index of basic variable that will leave the basis
                t = 1
                #find the first negative variable with b < 0
                for i in range(1, m):
                    if i != 0 and tableau[i][0] < 0:
                        t = i
                        break
                if all(tableau[t][i] >= 0 for i in range(1, n)):
                    infeasible = True
                    break
                else:
                    #choose the variable that will enter the basis
                    min = 100000
                    h = 1
                    for i in range(1, n):
                        if tableau[t][i] < 0 and tableau[0][i] / abs(tableau[t][i]) < min:
                            min = tableau[0][i] / abs(tableau[t][i])
                            h = i
                    if verbose == 2:
                        print('Pivot operation on the cell: {}\n'.format((t, h)))

                    #pivot operation
                    self.pivot_operation(t, h)

                    #update the vector beta, containing the indices of the basis variables
                    beta[t-1] = h

            #Print the intermediate tableau
            if verbose:
                print('TABLEAU:\n{}\n'.format(tableau))

        if optimal:
            #solution
            x = [0]*(n - 1)
            for i, b in enumerate(beta):
                x[b-1] = tableau[i+1][0]
                self.optimal = True
            self.solution = x
            self.z = -tableau[0][0]
            #print('The tableau has an optimal solution x = ', x)
        elif infeasible:
            self.infeasible = True
            #print('The tableau is infeasible')

    def solve(self, verbose=0):
        '''
        Solve the model.
        This function apply whatever method (simplex, gomory cut, ...) is necessary in order to solve the model.
        '''

        #start by using the primal simplex method
        self.primal_simplex_method(verbose=verbose)

        b = [self.tableau[i][0] for i in range(1, self.tableau.shape[0])]
        int_solution = all(elem == int(elem) for elem in b)
        #if it is not unbounded and there is at least an integer value start combining gomory cuts and dual simplex method
        if not self.unbounded and self.integer:
            #check if exists an integer value in the current solution
            if not int_solution:
                #set optimal to False since the solution it is not integer
                self.optimal = False
                #loop for finding integer solution if exists
                while not int_solution and not self.infeasible:
                    self.gomory_cut(verbose)
                    self.dual_simplex_method(verbose=verbose)
                    #set the new b
                    b = [self.tableau[i][0] for i in range(1, self.tableau.shape[0])]
                    int_solution = all(elem == int(elem) for elem in b)

#create a model object from external source like a txt file
def read_tableau(file_name):
        tableau = []
        #try to read the file
        f = open(file_name, 'r')
        #create tableau
        for line in f:
            row = line.split(' ')
            row = [int(x) for x in row]
            tableau.append(row)
        #close file
        f.close()

        #assign the created tableau to the object model
        tableau = np.array(tableau, dtype='float')
        basic_var = [0, 0]
        #return the model
        return Model(tableau=tableau, basic_var=basic_var)