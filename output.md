# OT_1.py VOGEL+MODI


rows: 3
cols: 4
cost matrix:
4 6 8 5
7 3 5 6
2 4 7 3
supply vector:
45 55 35
demand matrix:
50 30 25 30
[[20.  0.  0. 25.]
 [ 0. 30. 25.  0.]
 [30.  0.  0.  5.]]
cost: 465.0

Final:
[[ 0.  0. 15. 30.]
 [20. 30.  5.  0.]
 [30.  0.  5.  0.]]
Cost: 430.0


# OT_2.py    BIG M
number of variables: 4
minimise or maximise (min/max): max
objective coefficients:
35 25 40 30
number of constraints: 5
constraints (coeffs relation rhs per row):
1 2 1 1 <= 120
2 1 3 1 <= 180
1 2 2 1 <= 150
1 0 2 0 = 50
0 1 0 2 >= 30
Optimal solution found.
x1 = 50.0000
x2 = 20.0000
x3 = 0.0000
x4 = 50.0000
Objective value: 2850.0000