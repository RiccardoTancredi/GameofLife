import numpy as np
from constants import*

class Toroid:
    def __init__(self, grid=None, seed=None, period=None): 
        self.seed = seed if seed else np.random.seed(123)
        if grid:
            self.grid = grid
            self.length = grid.shape[0]
            self.height = grid.shape[1]
        else:
            self.length = ROWS
            self.height = COLS
            self.grid = self.create_grid()
        self.period = period

    def create_grid(self):
        grid = np.random.randint(2, size=(self.length, self.height))
        return grid

    def search_surround(self,pos):
        alive = 0
        x,y = pos[0]+1,pos[1]+1
        
        grid2 = np.pad(self.grid, pad_width=1)    
        grid2[0],grid2[-1] = grid2[-2],grid2[1] #first/last row = last/first row
        grid2[:,0], grid2[:,-1] = grid2[:,-2],grid2[:,1] #same w/ columns
        
        alive = alive + grid2[x-1][y-1] + grid2[x-1][y] + grid2[x-1][y+1]
        alive = alive + grid2[x][y-1] + grid2[x][y+1]
        alive = alive + grid2[x+1][y-1] + grid2[x+1][y] + grid2[x+1][y+1]
        return alive

    def neighbors(self):
        #neighbors = np.array([[self.search_surround([x,y]) for x in range(self.length)] for y in range(self.height)])
        neighbors = self.grid.copy()
        for i in range(self.length):
            for j in range(self.height):
                neighbors[i,j] = self.search_surround([i,j])
        return neighbors

    def get_cell(self, position):
        row, col = position
        if 0 <= row <= ROWS-1 and 0 <= col <= COLS-1:
            return self.grid[row][col]
        else:
            pass
    
    def get_cells(self, color=None):
        cells = []
        for i in range(ROWS):
            x = i * SQUARE_SIZE
            for j in range(COLS):
                y = j * SQUARE_SIZE 
                cell = self.get_cell((i, j))
                if not cell:
                    continue
                value = ((x, y), cell)
                cells.append(value)
        return cells
    
    def update(self): #to be merged with neighbors()
        neighbors = self.neighbors()
        old_grid = self.grid.copy()
        new_grid = old_grid
        for i in range(self.length): #could be done with masks
            for j in range(self.height):
              #1st rule: freeze
              if neighbors[i,j] == 2:
                new_grid[i,j] = old_grid[i,j]
              #2nd rule: birth    
              elif neighbors[i,j] == 3:
                new_grid[i,j] = 1
              #3rd rule: death
              else: new_grid[i,j] = 0
        self.grid = new_grid
        return new_grid

    def trailblaze(self, time): # "heatmap" ! work in progress !
        heat = self.grid    #np.zeros((self.length,self.height))
        for i in range(time):   #voglio istanti diversi = colori diversi e sovrapporre nuovo a vecchio
          old = np.where(heat>0, heat,0)
          new = self.update()
          heat = heat + i*np.where((new-old)>0, (new-old),0)
        return heat    

    def stampa(self):
        print(self.grid)


    # Search patterns
    
    def rotate_pattern(self, way, times):
        return np.rot90(way, times)

    def chiral(self, direction):    # direction could be up/down (0) or left/right (1)
        return np.flip(self.pattern, direction)

    def search_pattern(self, pattern, name):   #'pattern' is just a np.array
        pattern_trovati = []
        pattern_used = []
        self.pattern = pattern
        for chirality in range(0, 2):
            for rotation in range(0, 4): 
                tmp = self.chiral(chirality)
                pattern_used.append(self.rotate_pattern(tmp, rotation))
        pattern_used = np.unique(pattern_used)
        # search on grid
        for k in range(pattern_used.shape[0]):
            for i in range((self.length - self.pattern.shape[0] + 1)):
                for j in range((self.height - self.pattern.shape[1] + 1)):
                    looking_element = self.grid[i:self.pattern.shape[0]+i, j:self.pattern.shape[1]+j]
                    if (looking_element.astype(int) == pattern_used[k]).all():
                        # print("trovata corrispondenza")
                        pattern_trovati.append([name, chirality, rotation, i, j])
                    # print([pattern, chirality, rotation, i, j])
        return pattern_trovati