# GameofLife
Game of Life - Laboratory of Computational Physics - Mod A
Feltrin Antonio, Sardo Infirri Giosuè, Tancredi Riccardo, Toso Simone

## Introduction
*Conway's Game of Life* (GoL) is perhaps the most famous cellular automaton. The board consists of a grid of *cells*, each either *alive* or *dead*. At each step the board is updated according to the following rules:
	1. An alive cell with less than two live neighbours dies (i.e. its state goes from *alive* to *dead*)
	2. An alive cell with more than three live neighbours dies
	3. An alive cell with two or three live neighbours stays alive
	4. A dead cell with three live neighbours becomes alive.
	
### Our project
We implemented the rules of GoL in Python, simulating it with [periodic boundary conditions](https://link-url-here.org) .using the Pygame library to create the visual interface. Running `main.py`, the user can choose the initial configuration (details below) and look at how the game evolves. Finally, we analysed some observable quantities gathered from our games (occupancy, lifespan).

## The code
### Board definition 
The game's rules are defined in `board.py`, in which we define the `Toroid` class. The board of the game is pictured as a matrix of values in ${0,1}$, in which each entry represents a cell which is either *dead* (0) or *alive* (1). The class `Toroid` is called whenever we run a new game. Depending on what we want to do, we might want to randomly initialize the game or to start from a specific grid. For this purpose, the class constructor takes in input various parameters.

```python
class Toroid:
    def __init__(self, grid=None, seed=None, period=None, image=None, dimension=None, native=50): 
```
In order, we have:
* `grid`: a numpy array of rank 2 containing 0 (dead) and 1 (alive) entries. If `grid` is not `None`, then game's board is initialised to `grid`. 
* `seed`: seed for the random number generator, in case we want to randomly initialize the matrix.
* `dimension`: a list containing height and width of the grid, in case we want to randomly initialize the matrix.
* `native`: probability to initialize a cell as *alive*. The default value is 50 (50% probability).

The class contains various methods, called either when running the game or during analysis. The most important for running the game are `search_surround` and `update`. The `search_surround(self,pos)` method counts the number of alive neigbours for the cell indexed by `pos`. The `update(self)` method updates the grid, switching to 0 the cells who die, to 1 the cells who are born and keeping at 1 the cells who stay alive.

### draw.py

### main.py
In the file `main.py` we allow the user to choose how to initialize the board. The terminal prompts the user to choose among certain options; the user replies by writing the answer. 
At the beginning of the file, we define a dictionary called `pattern_zoo`. This dictionary contains, in the form of numpy arrays, the most common patterns which emerge in the game.

The choices are *random*, *fromTxt* and *easterEgg*. 
* *random*: randomly initialize the grid. The user is then asked to input the seed for the random number generator and the vertical and horizontal dimension of the grid. 
* *fromTxt*: initialize the grid to a specific configuration described in a `.txt` file, stored by the user in the `initial_patterns` folder. The format in which the file has to be written is the following:
	```
	dimx,dimy
	noise
	pattern_name,i,j,chir
	```
 






### Sources:

 
