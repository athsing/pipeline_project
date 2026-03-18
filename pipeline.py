import pulp
import matplotlib.pyplot as plt
import pandas as pd

n = 15

h = [0,
     51,67,61,55,40,45,20,22,20,42,60,42,25,28,22
]

distance = [i*100 for i in range(n)]

cut_cost = 150
fill_cost = 100
dump_cost = 70
borrow_cost = 120

width = 20
length = 100

area = width * length   # 2000


trial1 = [51,50,45,40,35,30,29,34,39,40,35,30,25,25,22]
trial2 = [51,53,57,55,50,45,40,35,30,31,26,27,25,25,22]


def compute_cost(profile):

    total_cut = 0
    total_fill = 0

    for i in range(n):
        diff = profile[i] - h[i+1]

        if diff < 0:
            total_cut += abs(diff) * area
        else:
            total_fill += abs(diff) * area

    dump = 0
    borrow = 0

    if total_cut > total_fill:
        dump = total_cut - total_fill
    else:
        borrow = total_fill - total_cut

    cost = (
        cut_cost * total_cut +
        fill_cost * total_fill +
        dump_cost * dump +
        borrow_cost * borrow
    )

    return cost, total_cut, total_fill, dump, borrow


cost1, c1, f1, d1, b1 = compute_cost(trial1)
cost2, c2, f2, d2, b2 = compute_cost(trial2)

print("\nTrial 1 Cost =", cost1)
print("Trial 2 Cost =", cost2)


def build_model():

    model = pulp.LpProblem("Pipeline", pulp.LpMinimize)

    x = pulp.LpVariable.dicts("x", range(1,n+1))
    cut = pulp.LpVariable.dicts("cut", range(1,n+1), lowBound=0)
    fill = pulp.LpVariable.dicts("fill", range(1,n+1), lowBound=0)

    dump = pulp.LpVariable("dump", lowBound=0)
    borrow = pulp.LpVariable("borrow", lowBound=0)

    model += x[1] == 51
    model += x[15] == 22

    for i in range(1,n):
        model += x[i+1] - x[i] <= 5
        model += x[i] - x[i+1] <= 5

    for i in range(2,n):
        model += x[i+1] - 2*x[i] + x[i-1] <= 6
        model += -(x[i+1] - 2*x[i] + x[i-1]) <= 6

    model += (x[2] - x[1]) - 4 <= 6
    model += 4 - (x[2] - x[1]) <= 6

    model += (-3) - (x[15] - x[14]) <= 6
    model += (x[15] - x[14]) - (-3) <= 6

    for i in range(1,n+1):
        model += x[i] == h[i] - cut[i] + fill[i]

    total_cut = pulp.lpSum(cut[i] for i in range(1,n+1))
    total_fill = pulp.lpSum(fill[i] for i in range(1,n+1))

    model += total_cut - total_fill == dump - borrow

    cost = (
        cut_cost * total_cut +
        fill_cost * total_fill +
        dump_cost * dump +
        borrow_cost * borrow
    )

    model += cost

    return model, x

def build_model_relaxed():

    model = pulp.LpProblem("PipelineRelaxed", pulp.LpMinimize)

    x = pulp.LpVariable.dicts("x", range(1,n+1))
    cut = pulp.LpVariable.dicts("cut", range(1,n+1), lowBound=0)
    fill = pulp.LpVariable.dicts("fill", range(1,n+1), lowBound=0)

    dump = pulp.LpVariable("dump", lowBound=0)
    borrow = pulp.LpVariable("borrow", lowBound=0)

    model += x[1] == 51
    model += x[15] == 22

    # relaxed grade 5 -> 5.5

    for i in range(1,n):

        if i == 8:   # station 8-9 relaxed

            model += x[i+1] - x[i] <= 5.5
            model += x[i] - x[i+1] <= 5.5

        else:

            model += x[i+1] - x[i] <= 5
            model += x[i] - x[i+1] <= 5

    for i in range(2,n):
        model += x[i+1] - 2*x[i] + x[i-1] <= 6
        model += -(x[i+1] - 2*x[i] + x[i-1]) <= 6

    model += (x[2] - x[1]) - 4 <= 6
    model += 4 - (x[2] - x[1]) <= 6

    model += (-3) - (x[15] - x[14]) <= 6
    model += (x[15] - x[14]) - (-3) <= 6

    for i in range(1,n+1):
        model += x[i] == h[i] - cut[i] + fill[i]

    total_cut = pulp.lpSum(cut[i] for i in range(1,n+1))
    total_fill = pulp.lpSum(fill[i] for i in range(1,n+1))

    model += total_cut - total_fill == dump - borrow

    cost = (
        cut_cost * total_cut +
        fill_cost * total_fill +
        dump_cost * dump +
        borrow_cost * borrow
    )

    model += cost

    return model, x


model, x = build_model()
model.solve()

opt_cost = pulp.value(model.objective)

solution = [pulp.value(x[i]) for i in range(1,n+1)]

print("\nOptimal Cost =", opt_cost)

model2, x2 = build_model_relaxed()
model2.solve()

print("Relaxed cost =", pulp.value(model2.objective))


grades = []
change = []

for i in range(n-1):
    grades.append(solution[i+1] - solution[i])

for i in range(1,n-1):
    change.append(grades[i] - grades[i-1])

change.insert(0,None)
change.append(None)

table = pd.DataFrame({
    "Station": range(1,n+1),
    "Distance": distance,
    "Original": h[1:],
    "Optimal": solution,
    "Grade": grades + [None],
    "ChangeGrade": change
})

print(table)

table.to_excel("optimal_solution.xlsx", index=False)
table.to_csv("optimal_solution.csv", index=False)


def plot_profile(profile, name, filename):

    plt.figure(figsize=(10,5))

    plt.plot(distance, h[1:], marker='o', label="Original")
    plt.plot(distance, profile, marker='s', label=name)

    plt.xlabel("Distance (m)")
    plt.ylabel("Elevation (m)")
    plt.title(name)

    plt.legend()
    plt.grid(True)

    plt.savefig(filename)
    plt.show()


plot_profile(trial1, "Trial 1", "trial1.png")
plot_profile(trial2, "Trial 2", "trial2.png")
plot_profile(solution, "Optimal", "optimal.png")


alt_solutions = []

for i in range(2,14):

    alt_model, x_alt = build_model()

    alt_model += alt_model.objective == opt_cost

    alt_model.sense = pulp.LpMaximize
    alt_model.setObjective(x_alt[i])

    alt_model.solve()

    sol = [pulp.value(x_alt[j]) for j in range(1,n+1)]

    if sol not in alt_solutions and sol != solution:
        alt_solutions.append(sol)

print("\nAlternate optimal solutions:", len(alt_solutions))

for s in alt_solutions:
    print(s)
