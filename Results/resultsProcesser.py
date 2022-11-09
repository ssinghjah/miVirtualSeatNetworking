import ast
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv

SEQUENCE_NUMBER_INDEX = 0

def parseLog(filePath, cleanLog = False):
    # Read input file
    f = open(filePath, "r")
    lines = f.readlines()
    f.close()

    nLines = len(lines)
    if nLines < 1:
        print("Invalid input file - please include at least one row")
        exit()
    data = []
    for line in lines:
        cells = line.strip().split(",")
        row = []
        for cell in cells:
            if "[" in cell:
                row.append(ast.literal_eval(cell))
            else:
                try:
                    row.append(float(cell))
                except ValueError:
                    row.append(cell)
        if cleanLog and row[3] != "Aggregated":
            continue
        data.append(row)
    return data