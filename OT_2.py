import numpy as np
import re

get_int = lambda: int(input())
get_ints = lambda: list(map(int, input().split()))
get_floats = lambda: list(map(float, input().split()))
get_str = lambda: input().strip()

EPS = 1e-9
M = 1e9

n = int(input("number of variables: "))
mode = input("minimise or maximise (min/max): ")

sign = -1 if "max" in mode else 1

print("objective coefficients:")
obj = get_floats()

m = int(input("number of constraints: "))

print("constraints (coeffs relation rhs per row):")

coef = []
rhs = []
rel = []

for i in range(m):
    line = get_str()
    line = line.replace("≥", ">=").replace("≤", "<=")

    parts = re.split(r"(<=|>=|=|<|>)", line)

    coef.append([float(x) for x in parts[0].split()])
    rel.append(parts[1])
    rhs.append(float(parts[2]))

cols = n

slack = {}
surplus = {}
artificial = {}

for i in range(m):

    if rel[i] == "<=":
        slack[i] = cols
        cols += 1

    elif rel[i] == ">=":
        surplus[i] = cols
        cols += 1

        artificial[i] = cols
        cols += 1

    else:
        artificial[i] = cols
        cols += 1

table = np.zeros((m, cols))

for i in range(m):

    table[i, :n] = coef[i]

    if rel[i] == "<=":
        table[i, slack[i]] = 1

    elif rel[i] == ">=":
        table[i, surplus[i]] = -1
        table[i, artificial[i]] = 1

    elif rel[i] == "=":
        table[i, artificial[i]] = 1

b = np.array(rhs, dtype=float)

cost = [0.0] * cols

for j in range(n):
    cost[j] = obj[j] * sign

for j in artificial.values():
    cost[j] = M

basis = []

for i in range(m):

    if rel[i] == "<=":
        basis.append(slack[i])
    else:
        basis.append(artificial[i])

for _ in range(1000):

    B = table[:, basis]

    x = np.linalg.solve(B, b)

    y = np.linalg.solve(
        B.T,
        [cost[j] for j in basis]
    )

    reduced = []

    for j in range(cols):
        reduced.append(cost[j] - table[:, j] @ y)

    enter = None

    for j in range(cols):
        if j not in basis and reduced[j] < -EPS:
            enter = j
            break

    if enter is None:

        ans = np.zeros(cols)

        for i, j in enumerate(basis):
            ans[j] = x[i]

        break

    d = np.linalg.solve(B, table[:, enter])

    if max(d) <= EPS:
        print("The problem is unbounded.")
        quit()

    leave = -1
    best = float("inf")

    for i in range(m):

        if d[i] > EPS:

            ratio = x[i] / d[i]

            if ratio < best:
                best = ratio
                leave = i

    basis[leave] = enter

possible = True

if "ans" in locals():

    for j in artificial.values():

        if ans[j] > EPS:
            possible = False

if "ans" not in locals():

    print("The problem is unbounded.")

elif not possible:

    print("The problem is infeasible.")

else:

    print("Optimal solution found.")

    for i in range(n):
        print("x%d = %.4f" % (i + 1, ans[i]))

    value = sum(
        obj[i] * ans[i]
        for i in range(n)
    )

    print("Objective value: %.4f" % value)