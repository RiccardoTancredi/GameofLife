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
The game's rules are defined in `board.py`, in which we define the `Toroid` class. The class `Toroid` is called whenever we run a new game. Depending on what we want to do, we might want to randomly initialize the game or to start from a specific grid. For this purpose, the class constructor takes in input various parameters.

```python
class Toroid:
    def __init__(self, grid=None, seed=None, period=None, image=None, dimension=None, native=50): 
```
In order, we have:
* `grid`: a numpy array of rank 2 containing 0 (dead) and 1 (alive) entries. If `grid` is not `None`, then game's board is initialised to `grid`. 
* `seed`: seed for the random number generator, in case we want to randomly initialize the matrix.
* `dimension`: a list containing height and width of the grid, in case we want to randomly initialize the matrix.
* `native`: probability to initialize a cell as *alive*. The default value is 50 (50% probability).






### Sources:

 
