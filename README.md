# Pipeline Optimization using Linear Programming

## Overview

This project solves a **pipeline vertical alignment optimization problem** using Linear Programming.

The goal is to determine the optimal elevation profile of a water pipeline across rolling terrain while satisfying all design constraints and minimizing total construction cost.

Constraints used:

- Maximum grade ≤ 5%
- Maximum change in grade ≤ 6%
- Fixed elevations at start and end stations
- Clearance width = 20 m
- Distance between stations = 100 m
- Earthwork cost for cutting, filling, dumping, borrowing

The optimal solution is obtained using **Python + PuLP (Linear Programming Solver)** and compared with manual trial solutions.


---

## Features

- Trial-and-error solutions
- Cost calculation for trial solutions
- Linear Programming optimisation
- Detection of alternate optimal solutions
- Graphs of vertical profiles
- Excel / CSV output tables


---

## Project Files
Description:

- `pipeline.py` → main script
- `trial1.png` → graph of trial solution 1
- `trial2.png` → graph of trial solution 2
- `optimal.png` → graph of optimal solution
- `optimal_solution.xlsx` → table of optimal elevations
- `optimal_solution.csv` → same table in csv


---

## Requirements

Install dependencies before running:
`pip install pulp matplotlib pandas openpyxl`

---

## How to Run

Run the script from the terminal:
`python pipeline.py`

Outputs generated:

- trial1.png
- trial2.png
- optimal.png
- optimal_solution.xlsx
- optimal_solution.csv
- cost of trial solutions
- optimal cost
- alternate optimal solutions


---

## Method Used

### Trial Solutions

Two feasible elevation profiles were generated manually
while satisfying grade and change-in-grade constraints.

Cost calculated using width* length *height difference between two adjacent stations

---

### Linear Programming Model

#### Decision variables:
`x_i = elevation at station i`
#### Constraints:
`|x(i+1) − x(i)| ≤ 5`
`|(x(i+1)-x(i)) − (x(i)-x(i-1)) | ≤ 6`
#### Cut/fill relation:
`x_i = h_i − cut_i + fill_i`
#### Objective:
##### Minimise:
  150 × cut +
	100 × fill +
		70 × dump +
		120 × borrow 

Solved using PuLP solver.


---

## Sensitivity Analysis

- Multiple optimal solutions found
- Relaxing the grade constraint reduces cost
- Extending alignment may reduce earthwork


---

## Authors
Team: CaseCrackers

---

## Notes

Multiple optimal solutions may exist because the LP solution lies on a flat optimal region.

The differences between solutions are very small (~1e-5 m) and do not affect the cost.
