import pulp

# Define the problem
problem = pulp.LpProblem("MyUpdatedProblem", pulp.LpMaximize)

# Define the variables
x = pulp.LpVariable("x", lowBound=0)  # x >= 0
y = pulp.LpVariable("y", lowBound=0)  # y >= 0

# Objective function
problem += 4*x + 3*y, "Objective"

# Original Constraints
problem += x + y <= 20, "Constraint1"
problem += x + 2*y <= 30, "Constraint2"

# New Constraint
problem += x + 2*y >= 15, "NewConstraint"

# Solve the problem
problem.solve()

# Print the status
print("Status:", pulp.LpStatus[problem.status])

# Print the optimal solution
print("x =", x.varValue)
print("y =", y.varValue)

# Accessing the dual values (Lagrange multipliers) of the constraints
for name, constraint in problem.constraints.items():
    print(f"Lagrange Multiplier (shadow price) of {name}: {constraint.pi}")
