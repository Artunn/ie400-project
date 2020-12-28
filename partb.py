from ortools.linear_solver import pywraplp
import pandas as pd

def partb():
    PROB_LIMIT = 0.60;
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()
 
    # Create the variables y,c and t.
    y = {}
    for i in range(V):
        for j in range(V):
            y[i, j] = solver.IntVar(0, 1, '') #Only 1 or 0

    c = {}
    for a in range(V):
        c[a] = solver.IntVar(0, 1, '') #Only 1 or 0

    t = solver.NumVar(0, infinity, '')

    #Create objective function
    objective = solver.Objective()
    objective.SetCoefficient(t, 1)
    objective.SetMinimization()

    # Every village must be assigned to a center village
    for i in range(V):
        solver.Add(solver.Sum([y[i, j] for j in range(V)]) == 1)

    # Total sum of the centers must be 4
    solver.Add(solver.Sum([c[j] for j in range(V)]) == 4)

    #  A village can be assigned to another village only if it is a center
    for i in range(V):
        for j in range(V):
            solver.Add(y[i, j] <= c[j])

    #The distance between the village and the center should be minimized
    for i in range(V):
        solver.Add(solver.Sum(d.iat[i, j] * y[i,j] for j in range(V)) <= t)

    #Probability of being out of use for a selected road must be smaller than 0.60.
    for i in range(V):
        for j in range(V):
            solver.Add(y[i, j] * p.iat[i,j] <= PROB_LIMIT)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        for i in range(V):
            if c[i].solution_value() == 1:
                print('Selected %dth village as a center' % (i+1))
        print('Objective value =', solver.Objective().Value())
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    xls = pd.ExcelFile('data.xlsx')
    d = pd.read_excel(xls, 'd', header=None)
    p = pd.read_excel(xls, 'p', header=None)
    V = 0;
    if(d.shape[0] == d.shape[1]):
        V = d.shape[0];
    else:
        exit(-1);
    partb()