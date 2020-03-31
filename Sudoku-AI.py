#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ortools.sat.python import cp_model
import random

cell_size = 3
line_size = cell_size**2
lines = range(line_size)

def solve_sudoku(local_puzzle):
    model = cp_model.CpModel()

    # Create IntVar for each position
    nonets = {}
    for i in lines:
        for j in lines:
            nonets[i, j] = model.NewIntVar(1, line_size, 'Nonet(%i, %i)' % (i, j))

    # All rows must be different
    for i in lines:
        model.AddAllDifferent([nonets[(i, j)] for j in lines])

    # All columns must be different
    for j in lines:
        model.AddAllDifferent([nonets[(i, j)] for i in lines])

    # All elements in nonet must be different
    for i in range(cell_size):
        for j in range(cell_size):
            cell = []
            for x in range(cell_size):
                for y in range(cell_size):
                   cell.append(nonets[(i * cell_size + x, j * cell_size + y)])
            model.AddAllDifferent(cell)

    # Get all cells different of 0 from the initial puzzles
    for i in lines:
        for j in lines:
            if local_puzzle[i][j] != 0:
                model.Add(nonets[(i, j)] == local_puzzle[i][j])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Possible status are INFEASIBLE, OPTIMAL and MODEL_INVALID
    res = []
    if status == cp_model.FEASIBLE:
        for i in lines:
            res.append([int(solver.Value(nonets[(i, j)])) for j in lines])
    return (status, res)


def generate_puzzle(n):

    # Empty puzzle
    local_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

    # Random point in the puzzle
    i,j = random.randint(0,8), random.randint(0,8)

    # Random digit at the point
    local_puzzle[i][j] = random.randint(0,8)

    # Solve the puzzle
    status, res = solve_sudoku(local_puzzle)

    # Then we fill the puzzle with 81-n cells init to 0
    nb = 81 - n
    while nb > 0:
        i,j = random.randint(0,8), random.randint(0,8)
        if (res[i][j] != 0):
            res[i][j] = 0
            nb-=1

    print("\nPuzzle to solve: \n")
    for k in range(9):
        print(res[k])

    print("\nPuzzle solved: \n")
    status, res = solve_sudoku(res)
    print("Status is " + str(status))
    if status == cp_model.FEASIBLE:
        for line in res:
            print(line)

# To Solve the matrix
def exo1():
    puzzle = [
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 4, 0, 7],
        [0, 0, 8, 0, 0, 0, 3, 0, 0],
        [0, 0, 1, 0, 9, 0, 0, 0, 0],
        [3, 0, 0, 4, 0, 0, 2, 0, 0],
        [0, 5, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 6, 0, 0, 0]
        ]
    status, res = solve_sudoku(puzzle)
    print("Status is " + str(status))
    if status == cp_model.FEASIBLE:
        for line in res:
            print(line)

# To generate matrix to solve with n number given
def exo2():
    n=eval(input("Number of cases given :\n"))
    generate_puzzle(n)

if __name__ == '__main__':
    print("\nExercice 1\n")
    exo1()
    print("\nExercice 2\n")
    exo2()
