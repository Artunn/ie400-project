from ortools.linear_solver import pywraplp
import pandas as pd

def partc():
    # Create the linear solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    infinity = solver.infinity()
    # Create the variable x
    x = {}
    for i in range(V):
        for j in range(V):
                x[i, j] = solver.IntVar(0, 1, '')

    # Dummy variable ui
    u = {}
    for i in range(1, V + 1):
        u[i] = solver.IntVar(1, V - 1, '')

    t = solver.NumVar(0, infinity, '')

    for i in range(V):
        solver.Add(solver.Sum([x[i, j] for j in range(V) if(i != j) ]) == 1)

    for j in range(V):
        solver.Add(solver.Sum([x[i, j] for i in range(V) if(i != j)]) == 1)

    for i in range(1, V):
        for j in range(1, V):
            if (i != j):
                solver.Add((u[i] - u[j] + x[i, j] * V) <= V - 1)

    #Probability of being out of use for a selected road must be smaller than 0.60.
    for i in range(V):
        for j in range(V):
            solver.Add(x[i, j] * p.iat[i,j] <= 0.60)

    #Objective function
    solver.Minimize(solver.Sum((d.iat[i, j] * x[i,j] for i in range(V) for j in range(V) if(i != j))));
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        print('Minimum time it takes =', solver.Objective().Value()/40)
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
    partc()