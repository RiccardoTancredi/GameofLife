#In this file we define the functions which, starting from an input .txt file, creates the desired grid. 
#For info on how to format the .txt file check README

import numpy as np
import matplotlib.pyplot as plt

def chiral(pattern, direction):    # Flip pattern
    return np.flip(pattern, direction)


def addPattern(matrix, occupiedMatrix_old, pos, pattern_old, random, chirality = False): # Adds pattern to input matrix (is called many times in the main)
    #go to pos (if it is in matrix) and add the pattern. 
    dims = matrix.shape #dimensions of matrix
    patternDims = pattern_old.shape #dimensions of pattern
    new_matrix = matrix.copy()
    occupiedMatrix = occupiedMatrix_old.copy()
    pattern = pattern_old.copy()

    if chirality: # Switches it 
        pattern = chiral(pattern, 1) # Switches left/right
    
    if pos[0] > dims[0] and pos[1] > dims[1]: # 1. Check if pos is in matrix
        print("Position has to be in matrix!\n")
        return matrix

    else: # 2. Take pattern --> take every square in pattern and calculate its position in matrix --> change accordingly    
        canWrite = True # Checks if it can write the pattern
        for i in range(patternDims[0]):
            for j in range(patternDims[1]):
                newPos = [(pos[0]+i)%dims[0],(pos[1]+j)%dims[1]] # Calculates where this square will end up on the toroid
                if occupiedMatrix[newPos[0], newPos[1]]:
                    print("You were overwriting a previous pattern") # Checks if the actual pattern is going to be loaded on another pattern
                    canWrite = False
                    break
                else:
                    new_matrix[newPos[0], newPos[1]] = pattern[i][j]
                    occupiedMatrix[newPos[0], newPos[1]] = True

        if canWrite:
            return new_matrix, occupiedMatrix
        else:
            return matrix, occupiedMatrix_old

def patternGenerator(patternArray, posArray, chirArray, dimensions, random = None):
    # Start from zero matrix --> add patterns in positions contained in array --> if random put randomly zeros and ones
    startingMatrix = np.zeros(dimensions)
    occupiedMatrix = np.full(dimensions, False)

    if random:
        startingMatrix = np.random.randint(0, 2, dimensions)
    
    for (pattern, pos, chir) in zip(patternArray, posArray,chirArray):
        startingMatrix, occupiedMatrix = addPattern(startingMatrix, occupiedMatrix, pos, pattern, random, chir)
    
    return startingMatrix

# def main(): # Main to check the good functioning of the program
#     patterns = [pattern_zoo['block'],pattern_zoo['loaf'],pattern_zoo['tub']]
#     positions = [(0,0),(0,4),(6,0)]
#     chiralities = [False, True, False]
#     matrice = patternGenerator(patterns, positions, chiralities, (11,11), random = False)
#     plt.imshow(matrice)

# main()

