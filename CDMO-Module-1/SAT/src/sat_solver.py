from tqdm import tqdm
from itertools import combinations
from plot_Solution import importInstances, plotSolution, outputSolution
from z3 import *
import time

#Input file
instances = importInstances("C:/Users/jyoti/Desktop/CDMO-Module-1_github/instances/")

def at_least_one(bool_vars):
    return Or(bool_vars)

def at_most_one(bool_vars):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]

def exactly_one(solver, bool_vars):
    solver.add(at_most_one(bool_vars))
    solver.add(at_least_one(bool_vars))

def DecisionVariables(instanceNumber):
    numberOfCircuits = int(instances[instanceNumber][1])
    circuitsWidth = []
    circuitsHeight = []
    for value in instances[instanceNumber][2:]:
        width, height = value.split(' ')
        circuitsWidth.append(int(width))
        circuitsHeight.append(int(height))
    width = int(instances[instanceNumber][0])
    minHeight = int(math.ceil(sum([circuitsWidth[c] * circuitsHeight[c] for c in range(numberOfCircuits)]) / width))
    maxHeight = sum(circuitsHeight)
    return numberOfCircuits, circuitsWidth, circuitsHeight, width, minHeight, maxHeight

def SAT(s, height):
    plate = [[[Bool(f"plate{i}_{j}_{c}") for c in range(numberOfCircuits)] for j in range(height)] for i in range(width)]
    for i in range(width):
        for j in range(height):
            s.add(at_most_one(plate[i][j]))
    for c in range(numberOfCircuits):
        positions = []
        for i in range(width - circuitsWidth[c] + 1):
            for j in range(height - circuitsHeight[c] + 1):
                positions.append(And([plate[ii][jj][c] for ii in range(i, i + circuitsWidth[c]) for jj in range(j, j + circuitsHeight[c])]))
        s.add(at_least_one(positions))

    sol = []
    if s.check() == sat:
        m = s.model()
        for i in range(width):
            sol.append([])
            for j in range(height):
                for c in range(numberOfCircuits):
                    if m.evaluate(plate[i][j][c]):
                        sol[i].append(c)
    return sol


for instanceNumber in tqdm(range(len(instances))):
    numberOfCircuits, circuitsWidth, circuitsHeight, width, minHeight, maxHeight = DecisionVariables(instanceNumber)
    height = minHeight
    solutionFound = False
    while not solutionFound and height <= maxHeight:
        s = Solver()
        times = 300 * 1000
        s.set(timeout=times)
        start = time.time()
        sol = SAT(s, height)
        end = time.time()
        print(end-start)
        if (sol) :
            start_x, flag, start_y= [False]*(numberOfCircuits), [False]*(numberOfCircuits), [False]*(numberOfCircuits)
            for i in range(len(sol)):
                for j in range(len(sol[0])):
                    for c in range(numberOfCircuits):
                        if sol[i][j] == c and not(flag[c]):
                            flag[c] = True
                            start_x[c] = i
                            start_y[c] = j
            circuits = [[circuitsWidth[i], circuitsHeight[i], start_x[i], start_y[i]] for i in range(numberOfCircuits)]
            plotSolution(width, minHeight, circuits, f'C:/Users/jyoti/Desktop/CDMO-Module-1_github/SAT/out/plot/plot-{instanceNumber + 1}.png')
            outputSolution(instances[instanceNumber], minHeight, start_x, start_y, f'C:/Users/jyoti/Desktop/CDMO-Module-1_github/SAT/out/out-{instanceNumber + 1}.txt')
            solutionFound = True
        height = height + 1
    if(not solutionFound):
        print("\nFailed to solve instance %i" % (instanceNumber + 1))