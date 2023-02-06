# Game of Life

Game of Life - Laboratory of Computational Physics - Mod A
Feltrin Antonio, Sardo Infirri Giosuè, Tancredi Riccardo, Toso Simone

<div align="center">
    <img src=figures/einstein.gif width=152 height 202>
    <img src=figures/mona.gif width=136 height 202>
    <img src=figures/orecchino.gif width=172 height 202>
</div>

## Introduction

*Conway's Game of Life* (GoL) is perhaps the most famous cellular automaton. The board consists of a grid of *cells*, each either *alive* or *dead*. At each step the board is updated according to the following rules:

1. Survivals: An alive cell with two or three neighbours survives for the next generation.
2. Births: A cell with three live neighbours becomes alive.
3. Deaths: An alive cell with more than three live neighbours dies from overpopulation and an alive cell with only one or zero neighbours dies from isolation (goes from *alive* to *dead*).

```python
#1st rule: survivals
if neighbors[i,j] == 2:
	new_grid[i,j] = old_grid[i,j]
#2nd rule: births
elif neighbors[i,j] == 3:
	new_grid[i,j] = 1
#3rd rule: deaths
else: 
	new_grid[i,j] = 0
```

### Our project

We implemented the rules of GoL in Python, simulating it with periodic boundary conditions and using the `Pygame` library to create the visual interface. Running `main.py`, the user can choose the initial configuration (details below) and look at how the game evolves. Finally, we analysed some observable quantities gathered from our games (such as _occupancy_ and _lifespan_).

## The code

### Board definition (board.py)

The game's rules are defined in `board.py`, in which the `Toroid` class is defined. The board of the game is pictured as a matrix of values in $\{0,1\}$, in which each entry represents a cell which is either *dead* (0) or *alive* (1). The class `Toroid` is called whenever we run a new game. Depending on what we want to do, we might want to randomly initialize the game or to start from a specific grid. For this purpose, the class constructor takes in input various parameters.

```python
class Toroid:
    def __init__(self, grid=None, seed=None, image=None, dimension=None, native=50): 
```

In order, we have:

* `grid`: a numpy array of rank 2 containing 0 (dead) and 1 (alive) entries. If `grid` is not `None`, then game's board is initialised to `grid`.
* `seed`: seed for the random number generator, in case we want to randomly initialize the matrix.
* `dimension`: a list containing height and width of the grid, in case we want to randomly initialize the matrix.
* `native`: probability to initialize a cell as *alive*. The default value is 50 (50% probability).
* `image`: an extra parameter which is called in case the user wants to initialize the board by reading an image (more on that later). It is quite slow and requires the image to be written in the RGB format, so this kind of game initialization was only used for generating some specific patterns which are now stored in the `images_txt` folder.

The class contains various methods, called either when running the game or during analysis. The most important for running the game are `search_surround` and `update`. The `search_surround(self, pos)` method counts the number of alive neigbours for the cell indexed by `pos`. The `update(self)` method updates the grid, switching to 0 the cells who die, to 1 the cells who are born and keeping at 1 the cells who stay alive.

### Board analysis (_board.py_)

In the Game of Life the board transitions from a disordered soup to a constellation of ordered structures (patterns).  Patterns can live forever if nothing interferes with them, and they belong to one of three classes:

* still lifes: as the name suggests, they stay still.
* oscillators: they change forms, returning cycliclally to the first one every _T_ iterations. _T_ is called _period_.
* spaceships: they travel across the board.

The `board.py` file contains functions and variables used to analyse the game. We'd defined _occupancy_ $o(t)$ as the number of cells alive at a particular time and _heat_ $h(t)$ as the sum of born and dead cells at time $t$.
The `search_patterns` function counts the number of occurrencies of a given pattern in the whole board at a given moment. We need to take into account the toroidal structure of the board: in order to do so, we expand it with the `Ipad` function. In this way we can find patterns that are split by the edge of the board. `search_patterns` also considers flipped and rotated variants of the desired pattern.

<div align="center">
    <img src=figures/bee_hive_filter.png width=450 height 300>
    <img src=figures/beeedge.png width=450 height 300>
</div>

Patterns are stored in rectangular filters as the one displayed above. The `search_patterns` function looks for matches of the filter in the padded board, without considering the grey cells (0.5 value) in the filter. This guarantees a standardized match formatting, since the position of the match refers to the top left corner of the filter, while allowing a flexible filter shape. Let's take for example the right image above: the _beehive_ is found on the edge, thanks to the padding on the board, in the position marked by the red rectangle. The filter (green rectangle) doesn't consider the bottom left square (blue rectangle), thus correctly classifying what it sees as a _beehive_.

### _draw.py_

In order to graphically see our board, we have used `pygame` to display the game evolution. The `Draw class` takes in input the `display.set_mode` function, containing the dimensions of the window and the `Toroid` class.

```python
class Draw:
    def __init__(self, window, game):
```

The latter variable is essential to use the grid info (alive and dead cells): to draw the alive (white) cells, the `draw_cells` method from `Toroid` is used in order to convert the position on the grid to that in pixels on the pygame window.

### _main.py_

In the file `main.py` we allow the user to run the game, choosing how to initialize the board. The terminal prompts the user to choose among certain options.

The choices are *random*, *fromTxt* and *easterEgg*.

* *random*: randomly initialize the grid. The user is then asked to input the seed for the random number generator and the vertical and horizontal dimension of the grid, followed by the initial nativity (i.e. the percentage of alive cell at the beginning of the game).
* *fromTxt*: initialize the grid to a specific configuration described in a `.txt` file, stored by the user in the `initial_patterns` folder. The format in which the file has to be written is the following:

  ```txt
  dim_ver,dim_hor
  noise
  pattern_name1,i1,j1,chir1
  pattern_name2,i2,j2,chir2
  pattern_name3,i3,j3,chir3
  ...

  ```

  `dimx` and `dimy` are the height and width of the grid; `noise` is either `True` or `False` and selects whether we want to add random noise (i.e. random is on the grid with probability 0.5) to the board. Finally, the last rows position patterns from `pattern_zoo` in desidered positions: for example, the row

  ```
  loaf,0,4,True
  ```

  positions the pattern named *loaf* with its top left corner on cell (0,4); the boolean value `chir` ("chirality") chooses whether we want to flip the pattern around the vertical axis (`True`) or keep it as it is written in the dictionary. The function called to generate the grid starting from the .txt file is defined in `pattern_generator.py`.
* *easterEgg*: We added this option just for fun. The terminal asks to input a keyword among a certain list of special patterns (*monalisa*,*einstein*,...) such as the one displayed at the beginning of this README. The initial configurations where simply obtained by reducing the size of a photo to the desired number of pixels and then running [Floyd-Steinberg Dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering) to convert each pixel to a black/white value (code in `image_generator.py`).

## Data analysis

In this section we present the results we got by analysing the data gathered by running the game on various grid sizes and with different initial configurations. All the data below are analized in the files `lifespan.ipynb` and `occurences_lifetimes.ipynb`

### Average board lifespan

Since the rules of the game are deterministic, if the board finds itself in the same configuration at two different steps it will enter a loop. We say that the evolution has *stabilized* when it enters an infinite loop. We can therefore define the *lifespan* of an initial configuration as the number of steps it takes for it to enter a loop. [Nathaniel Johnston](http://www.njohnston.ca/2009/07/the-maximal-lifespan-of-patterns-in-conways-game-of-life/) observed that, when fixing a certain nativity value, the distribution of  lifespans tend to decay exponentially. We recall that the *nativity* is the probability for a cell to be alive in the initial configuration. In the following graph we show the distributions we found by running the game on various nativities, keeping a grid of $15 \times 15$. The weighted average of the exponents of the fits is $-0.0118 \pm  0.0001$; all the exponents are within $3\sigma$ of the weighted mean, the nativity does not seem to affect the decay of the lifespan distribution. The data was generated in `lifespan.py`.

<div align="center">
    <img src=plot_analysis/lifespan_fit_125.png width=152>
    <img src=plot_analysis/lifespan_fit_250.png width=152>
    <img src=plot_analysis/lifespan_fit_375.png width=152>
    <img src=plot_analysis/lifespan_fit_500.png width=152>
    <img src=plot_analysis/lifespan_fit_625.png width=152>
</div>

We are also interested in checking how the *average* lifespan varies with respect to the nativity. By varying the nativity in the range ($5\%, 98\%$) and averaging across 1000 games on each nativity we get the following graph. The data for this graph was generated in `many_nativities.py`.

<div align="center">
    <img src=plot_analysis/nativity_lifespan.png height=202>

</div>

We see that the lifespan hits a maximum around $40\%$ (in particular, the maximum value obtained corresponds to a nativity of $37.5\%$).This result is not unexpected, considering that a new cell is born if $3/8 = 37.5\%$ of its neighbours are alive, as observed [in this blog post](http://www.nathanieljohnston.com/2009/06/longest-lived-soup-density-in-conways-game-of-life/).
*This analysis was performed in the* `lifespan.py` *notebook.*

### Asymptotic occupancy

As the grid evolves, occupancy decreases until the grid enters a loop. We can take the average occupancy during this loop and see how it behaves with respect to the initial nativity. For this purpose, we ran the game with nativities between $5\%$ and $98\%$, using 300 different initial configurations for each nativity and calculating the asymptotic occupancies. The data for this analysis was generated in `nativity_occupancy.py`. One can see the behaviour of the data in the following plot:

<div align="center">
    <img src=plot_analysis/nativity_occupancy.png height=280>
    <img src=figures/nativity_occupancy.jpg height=280>
    <!-- <img src=plot_analysis/linear_fit.png height=280> -->
</div>

This result is in accordance with the result found [in the following paper](https://www.sciencedirect.com/science/article/abs/pii/037843719190277J) and pictured in the previous image. The graph shows that, for a nativity of $37.5\%$, we expect that the final occupancy is directly proportional to the grid size $n \times n$, with a coefficient of around $0.3$. One can see this behaviour by plotting the asymptotic occupacy with respect to the area of the grid, as pictured below. The data is generated in `occupances_analysis.py`.

<div align="center">
    <img src=plot_analysis/linear_fit.png height=300>
</div>

The angular coefficient is $0.0317 \pm 0.0003$, in accordance with the results found in the previous linked paper.

### Occupancy and Heat analysis

Togther with the _Average lifespan_ analysis we have have also computed an analysis based on **occupancy** and **heat**.

<div align="center">
    <img src=plots/15_15.png height=300>
</div>

We can see how, as expected by its definition, heat follows occupancy. The fit is performed by considering a model for population expansion with a maximum carrying capacity $K$, given by the following logistic equation 

$$
\dot{x}=rx(1-\frac{x}{K})
$$

 where $r$ is the rate of reproduction in absence of density regulation.
Even though this model is not actually built for the game of life itself which has its own deterministic rules, the solution to the differential equation, $x(t)=\frac{Kx_0e^{rt}}{K+x_0(e^{rt}-1)}$ represents a good fit of our data, since an exponeential fit does not take into account the fact that, as shown in all our simulations, there can still be a fraction of alive particles, even after long time: this is of course reasonable since we are considering finite dimension grids.
We have found that the fraction of particles still alives $K=x(t\to\infty)$ goes quadratic with the dimension of the grid, which is coherent with what we found in the section *Asymptotic occupancy*.

### Pattern frequency

Another possible analysis is the extimation of pattern frequency, an indicator of how many times a specific _pattern_ appears through a run. The [Conway Life wiki](https://conwaylife.com/wiki/Common) doesn't have a clear-cut definition of frequency and commonness, so we'll use the one that follows. At each timestep $t_i$, we count the number of occurrencies $N_i(P)$ that a pattern _P_ is found across the grid, and we compute the total findings $N_{tot}(P) = \sum_{i=0}^{t_{max}} N_i(P)$. Patterns found in the same board position _(x,y)_ at consecutive timesteps are thus counted as different findings.

Having defined what are _occurrences_, we can now take the definition of relative frequency as written in the [LifeWiki](https://conwaylife.com/wiki/Relative_frequency): occurrences of a particular item divided by the total occurrences of all items in a set.

We have run many simulations in order to either estimate these frequencies but also to select hyperparameters such as the grid dimensions, the initial fraction of alive cells and the random seeds so that at $t_0$ each board starts with a random configuration.

After the before mentioned analysis on `average lifespan`, we have cycled among 100 seeds and 6 different grid squared dimensions (from `15x15` to `40x40`) for _500_ timesteps. Using the `search_pattern` function we have looked for the most common patterns. [Achim Flammenkamp](http://wwwhomes.uni-bielefeld.de/achim/freq_top_life.html) compiled a list of the 100 most common _still lifes_, _oscillators_ and _spaceships_ by evolving almost 2 millions seeds on a 2048×2048 torus.

| dimension |    block |  blinker | bee_hive |      loaf |      boat |        tub |        pond |       ship |        toad |      beacon |
| :-------- | -------: | -------: | -------: | --------: | --------: | ---------: | ----------: | ---------: | ----------: | ----------: |
| [15, 15]  | 0.355779 | 0.297304 | 0.153612 | 0.0834919 | 0.0748238 |  0.0155743 | 5.28541e-05 |  0.0087914 |  0.00017618 |  0.00340028 |
| [20, 20]  |  0.36327 | 0.352436 | 0.110703 | 0.0731753 | 0.0681511 | 0.00936207 |  0.00780006 | 0.00944166 | 0.000139287 | 0.000149236 |
| [25, 25]  | 0.326815 | 0.353444 | 0.170124 | 0.0531898 | 0.0544692 |  0.0134903 |   0.0147258 | 0.00903743 | 0.000426471 |  0.00102855 |
| [30, 30]  | 0.357765 | 0.343675 | 0.149228 | 0.0456734 | 0.0550285 |  0.0161571 |   0.0144974 |  0.0114546 | 0.000553233 |  0.00182295 |
| [35, 35]  | 0.339015 | 0.354048 | 0.166334 | 0.0565936 | 0.0482382 |  0.0119482 |   0.0135322 | 0.00517336 | 0.000692798 | 0.000306363 |
| [40, 40]  | 0.360765 | 0.329482 | 0.160887 |  0.053141 | 0.0589856 |   0.013766 |   0.0108545 | 0.00655215 | 0.000586075 | 0.000367309 |

The results here obtained are in good agreement with those found in the research above mentioned and it is clear to see the higher the dimension of the toroidal grid the better the compatibility between the results. In particular we notice both the `block` and the `blinker` as the most frequent patterns with a relative frequency of ~ $33\%$.

<div align="center">
    <img src=plots/all_all.png height="50%" width="50%">
</div>

We also tried expanding the board into a 100x100, also running the simulation for _500_ timesteps. This time the sample size is reduced to only 57 different seeds due to the long computational time needed for such board dimensions.

| dimension  |    block |  blinker | bee_hive |      loaf |      boat |       tub |       pond |       ship |        toad |      beacon |
| :--------- | -------: | -------: | -------: | --------: | --------: | --------: | ---------: | ---------: | ----------: | ----------: |
| [100, 100] | 0.335997 | 0.348252 | 0.160406 | 0.0615305 | 0.0571706 | 0.0140943 | 0.00923986 | 0.00760617 | 0.000559395 | 0.000717659 |

As expected the results are in better agreement with the above cited articles.

#### Average pattern lifetime

In doing so we have to keep in mind that there is the risk of overestimating these results: this is due to the fact that it can happen that "stability" is reached in a few generations

We also asked ourselves the average time of a particular pattern to be alive. We extend the above mentioned analysis on pattern frequency by considering as occurrency: if a pattern appears in a particular position _(x, y)_ and with a particular chirality for $m$ consecutive time steps we just count it once with a lifetime of $m$(instead of counting it $m$ times as before). Doing this, we have estimated the average lifetime of each pattern.

| dimension |   block | bee_hive |    loaf |    boat |    ship |     tub |    pond | blinker |    toad |  beacon |
| :-------- | ------: | -------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| [15, 15]  | 33.0507 |  89.8866 | 131.639 | 64.3485 | 35.6429 |    44.2 |     1.5 | 15.0939 |       1 |     193 |
| [20, 20]  | 22.1023 |   44.508 | 57.4609 | 47.9021 | 30.6129 | 22.4048 | 26.1333 | 11.2101 | 1.16667 |   1.875 |
| [25, 25]  | 16.7395 |  49.9558 | 36.3991 | 29.0468 | 24.0167 |  16.937 | 46.0392 | 9.19798 |    2.72 | 13.6667 |
| [30, 30]  | 15.5673 |  36.1626 | 25.7596 | 26.3232 | 28.7045 | 18.1786 | 38.0595 | 7.40189 | 2.30189 | 23.6471 |
| [35, 35]  | 14.4415 |  37.7393 | 28.8227 | 23.0166 | 11.2576 | 12.8539 | 32.6639 | 7.22382 | 2.61842 |     5.5 |
| [40, 40]  | 14.3508 |  33.6934 | 27.2144 | 26.1871 | 12.9043 | 14.1191 |  30.447 | 6.43836 | 2.85526 | 4.85714 |

The average lifetime of each pattern decreases with the dimension of the grid

### Sources:

* _"Evolutionary dynamics: exploring the equations of life", Nowak, Martin A., 2006, Harvard university press;_
* _Conway Life Wiki:_ [https://conwaylife.com](https://conwaylife.com/wiki/Main_Page);
* _Nathaniel Johnston's blog:_ [http://www.nathanieljohnston.com/2009/06/longest-lived-soup-density-in-conways-game-of-life/](http://www.nathanieljohnston.com/2009/06/longest-lived-soup-density-in-conways-game-of-life/).
