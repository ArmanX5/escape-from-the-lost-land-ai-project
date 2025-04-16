# Phase-3: Escape from the Lost Land - Minimum Loss Pathfinding

This phase implements an A* search algorithm to find the optimal path that minimizes the amount of coins stolen by thieves in the game map.

## Project Structure
- `main.py`: Entry point of the program
- `map_loader.py`: Handles loading and parsing of game map files
- `a_star_solver.py`: Implements the A* search algorithm
- `utils.py`: Contains utility classes and functions
- `map.txt`: Sample game map file

## Game Rules
- The map is an NxN grid where each cell can contain:
  - Positive numbers: Treasure cells
  - Negative numbers: Cost cells
  - "!": Thief cells
- Aryan starts from (0,0) and must reach (N-1, N-1)
- Movement is restricted to right and down only
- When a thief is encountered:
  - The thief follows Aryan until reaching a cell with coins
  - The thief steals those coins and leaves
  - If another thief is encountered while one is following, they fight and both leave

## Implementation Details

### Node Class (`utils.py`)
Represents a state in the search space with:
- Current position (r, c)
- Thief status (has_thief)
- Path costs (g_cost, h_cost)
- Parent reference for path reconstruction

### A* Search Implementation (`a_star_solver.py`)
- Uses a priority queue based on f-cost (g + h)
- Maintains visited states to avoid cycles
- Generates successor states considering:
  - Movement restrictions (right/down)
  - Thief interactions
  - Cost calculations

### Map Loading (`map_loader.py`)
- Parses text files into NumPy arrays
- Handles special characters ("!" for thieves)
- Validates map dimensions and format

## Usage
1. Create a map file (e.g., `map.txt`) with the game grid
2. Run the program:
```python
python main.py
```

## Output
The program will output:
- The loaded map dimensions
- The optimal path found
- Total coins collected by Aryan
- Total coins stolen (minimized)

## Example Map Format
```
-3 ! -2 -2
-3 -2 ! 3
! 10 -8 !
-4 -6 ! -5
```
Where:
- Numbers represent coin values or costs
- "!" represents thief locations