import pulp


x = pulp.LpVariable('x', cat=pulp.LpInteger, lowBound=0)
y = pulp.LpVariable('y', cat=pulp.LpInteger, lowBound=0)

problem = pulp.LpProblem('Flexible_Network_Slicing', pulp.LpMinimize)

problem += 3 * x + 4 * y, 'Objective'

problem += x + 2 * y <= 20, 'Constraint 1'

problem += x + y >= 10, 'Constraint 2'

problem += x <= 15, 'Constraint 3'
solver = pulp.CPLEX_CMD(path=r"C:\Program Files\IBM\ILOG\CPLEX_Studio_Community2211\cplex\bin\x64_win64\cplex.exe")

problem.solve(solver)


print(x.value())
print(y.value())



