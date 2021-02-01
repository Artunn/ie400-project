from ortools.linear_solver import pywraplp
import pandas as pd

def partd():
    # Create the linear solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    infinity = solver.infinity()
    # Create the variable x
    x = {}
    for i in range(V):
        for j in range(V):
                x[i, j] = solver.IntVar(0, 1, '')

    m = solver.IntVar(0,30,'');

    y = {}
    for i in range(V):
        for j in range(V):
            y[i,j] = solver.NumVar(0, infinity, '')

    # c = {}
    # for i in range(0, V):
    #     c[i] = solver.IntVar(0, 1, '')

    solver.Add(solver.Sum(x[0, j] for j in range(1, V) if i != j) == m)

    solver.Add(solver.Sum(x[i, 0] for i in range(1, V) if i != j) == m)

    for j in range(1, V):
        solver.Add(solver.Sum(x[i, j] for i in range(V) if i != j) == 1)

    for i in range(1, V):
        solver.Add(solver.Sum(x[i, j] for j in range(V) if i != j) == 1)

    for i in range(1, V):
        solver.Add(solver.Sum(y[i, j] for j in range(V) if i != j)
                   - solver.Sum(y[j, i] for j in range(V) if i != j)
                   - solver.Sum(d.iat[i, j] * x[i,j] for j in range(V)) == 0
                   )

    for i in range(V):
        for j in range(V):
            solver.Add(y[i,j] <= 400 * x[i,j])

    for j in range(1, V):
        solver.Add(y[0,j] == d.iat[0,j] * x[0,j]);

    #Objective function
    solver.Minimize(m)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        for i in range (V):
            for j in range(V):
                print(x[i,j].solution_value())
    else:
        print('The problem does not have an optimal solution.')

if __name__ == '__main__':
    xls = pd.ExcelFile(r'C:\Users\Monster\Desktop\Bilkent Stuff\IE400\Project\data.xlsx')
    d = pd.read_excel(xls, 'd', header=None)
    p = pd.read_excel(xls, 'p', header=None)
    V = 0;
    if(d.shape[0] == d.shape[1]):
        V = d.shape[0];
    else:
        exit(-1);
    partd()