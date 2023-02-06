#In this file we define the Toroid class, which is called everytime we want to run the game. 

import numpy as np
from constants import*
from image_generator import gridFromImage

class Toroid:
    def __init__(self, grid=None, seed=None, image=None, dimension=None, native=50): # Parameters of the Toroid class defined in the README
        self.seed = np.random.seed(seed) if seed else np.random.seed(123) 
        self.image = image
        self.native = native #probability to be 1 in initial configuration
        if grid is not None:
            self.grid = grid
            self.length = grid.shape[0]
            self.height = grid.shape[1]
        else:
            self.length, self.height = dimension if dimension else [ROWS, COLS]
            self.grid = self.create_grid()
        self.occupancy = np.sum(self.grid)
        self.heat = 0

    def create_grid(self): # Creates the grid when one doesn't give a grid in input (from a image or from a random seed)
        if self.image:
            return gridFromImage(self.image, resize=True, desiredDimension=100)
        chance_grid = np.random.randint(low=0, high=100, size=(self.length, self.height))
        grid = np.where(chance_grid<self.native, 1, 0) # Chooses which cells to leave alive (with mean = percentage of native)
        return grid

    def search_surround(self,pos): #Counts alive neighbours for cell at position pos
        alive = 0
        x,y = pos[0]+1,pos[1]+1
        
        grid2 = np.pad(self.grid, pad_width=1)    
        grid2[0],grid2[-1] = grid2[-2],grid2[1]             #first/last row = last/first row
        grid2[:,0], grid2[:,-1] = grid2[:,-2],grid2[:,1]    #same w/ columns
        
        alive = alive + grid2[x-1][y-1] + grid2[x-1][y] + grid2[x-1][y+1]
        alive = alive + grid2[x][y-1] + grid2[x][y+1]
        alive = alive + grid2[x+1][y-1] + grid2[x+1][y] + grid2[x+1][y+1]
        return alive # Returns an integer number from 0 to 8

    def neighbors(self): #Find neighbours for each cell
        #neighbors = np.array([[self.search_surround([x,y]) for x in range(self.length)] for y in range(self.height)])
        neighbors = self.grid.copy()
        for i in range(self.length):
            for j in range(self.height):
                neighbors[i,j] = self.search_surround([i,j])
        return neighbors

    def get_cell(self, position): # for pygame: finds a single cell
        row, col = position
        if 0 <= row < self.length and 0 <= col < self.height:
            return self.grid[row][col]
        else:
            pass
    
    def get_cells(self, color=None): # for pygame: it creates the grid that pygame takes as input
        cells = []
        for i in range(self.length):
            x = i * SQUARE_SIZE
            for j in range(self.height):
                y = j * SQUARE_SIZE 
                cell = self.get_cell((i, j))
                if not cell:
                    continue
                value = ((x, y), cell)
                cells.append(value)
        return cells
    
    def update(self): # Update function according to rules of the game 
        neighbors = self.neighbors()
        old_grid = self.grid.copy()
        new_grid = self.grid.copy()
        self.occupancy = 0
        self.heat = 0
        for i in range(self.length): # 
            for j in range(self.height):
              #1st rule: survivals
              if neighbors[i,j] == 2:
                new_grid[i,j] = old_grid[i,j]
              #2nd rule: births    
              elif neighbors[i,j] == 3:
                new_grid[i,j] = 1
              #3rd rule: deaths
              else: 
                new_grid[i,j] = 0
        self.grid = new_grid
        
        self.occupancy = np.sum(self.grid)
        self.heat = np.sum(np.abs(new_grid-old_grid))
        
        return new_grid

    # Search patterns
    def Ipad(self, n): #Pads the board in a way that satisfies Periodic Boundary Conditions 
        # n = rows of padding
        grid2 = np.pad(self.grid, pad_width=n)    
        for i in range(n):
            grid2[-i+n-1] = grid2[-n-1-i]       # first row = last row
            grid2[i-n] = grid2[n+i]             # last row = first row
        for i in range(n):
            grid2[:, -i+n-1] = grid2[:, -n-1-i]       # first row = last row
            grid2[:, i-n] = grid2[:, n+i]             # last row = first row
        return grid2
    
    def rotate_pattern(self, way, times): # Rotates the pattern clockwise
        return np.rot90(way, times)

    def chiral(self, direction):    # Flips the pattern: direction could be up/down (0) or left/right (1)
        return np.flip(self.pattern, direction)

    # NB: 'pattern' is just a np.array
    def search_pattern(self, pattern): # Searches a determined pattern across the entire grid (even though it is flipped or rotated)
        pattern_trovati = []
        pattern_used = []
        self.pattern = pattern
        for chirality in range(0, 2):
            for rotation in range(0, 4): 
                tmp = self.chiral(chirality)
                pattern_used.append([self.rotate_pattern(tmp, rotation), chirality, rotation])
        pattern_used = myunique(pattern_used)

        # search on grid
        # In order to look also for pattern in the extreme part of the grid, we pad the grid itself 
        n = round(self.pattern.shape[0]/2)
        tmp_grid = self.Ipad(n)
        for k in range(len(pattern_used)):
            for i in range((tmp_grid.shape[0] - pattern_used[k][0].shape[0])):
                for j in range((tmp_grid.shape[1] - pattern_used[k][0].shape[1])):
                    looking_element = tmp_grid[i:pattern_used[k][0].shape[0]+i, j:pattern_used[k][0].shape[1]+j]
                    if not ((np.round(np.abs(looking_element.astype(int) - pattern_used[k][0]))).any()):
                        # print("trovata corrispondenza")
                        chirality, rotation = pattern_used[k][1:3]
                        pattern_trovati.append([chirality, rotation, i, j])
        return pattern_trovati

def myunique(listofarr): # Removes the counted patterns that have been counted more than once (example: rotated of 180° and flipped is equal to the initial one)
    n = len(listofarr) 
    uniquelist = [listofarr[0]]
    for i in range(1, n):
        count = 0
        for arr in uniquelist:
            if np.abs(listofarr[i][0].shape[0] - arr[0].shape[0]):  # if pattern.shape is different the patterns are different
                count += 1
            elif (listofarr[i][0] - arr[0]).any():
                count += 1
        if count == len(uniquelist):
            uniquelist.append(listofarr[i])
    return uniquelist # Returnes the list of patterns that are all different (removed the multiple counted)