# Escape from the Lost Land - Phase 1 Documentation

## Project Overview

This project implements a pathfinding solution for a game called "Escape from the Lost Land" (فرار از سرزمین گمگشتگان). The game features a character named Arian who must navigate through a grid-based world with various challenges including treasures, thieves, and costs.

## Problem Description

The game world is represented as an n×n matrix where each cell can be one of three types:

1. Normal cells: Represented by negative numbers indicating the cost to pass through
2. Treasure cells: Represented by positive numbers indicating gold coins to collect
3. Thief cells: Represented by "!" symbol where thieves can be encountered

### Movement Rules

- Movement is restricted to Down and Right directions only
- The journey always starts at (0,0) and ends at (n-1,n-1)
- When encountering a thief:
  - The thief joins Arian until the next cell
  - If the next cell has treasure, the thief steals it
  - If the next cell is normal, the thief steals the cost amount
  - If encountering another thief while already having one, the thieves fight and Arian escapes without loss
  - After leaving Arian's vehicle, thieves return to their original positions

## Implementation Details

### Input Format

The program accepts input in the following format:

```
n
a11 a12 ... a1n
a21 a22 ... a2n
...
an1 an2 ... ann
```

Where:

- n is the size of the grid
- aij represents the cell values (negative numbers for costs, positive for treasures, "!" for thieves)

### Current Implementation (Phase 1)

The current implementation focuses on Objective 1: Finding a path from start to end while ignoring treasures and thieves.

#### Key Components:

1. `parse_input()`: Reads and validates the grid configuration from standard input
2. `solve_objective1()`: Implements a BFS algorithm to find a valid path from (0,0) to (n-1,n-1)

#### Algorithm Details:

- Uses Breadth-First Search (BFS) to find the first valid path
- Tracks visited cells to avoid cycles
- Calculates final coins and stolen amount for the found path
- Provides detailed path description with moves and cell values

### Output Format

For the current implementation, the output includes:

1. The complete path from start to end
2. Each move (Down/Right) with the cell value
3. Final coin count
4. Total amount stolen by thieves

## Example

Input:

```
4
-3 -2 -2 !
3 -2 3 -2
10 -8 ! 1
-4 -3 -6 !
```

Output includes:

- Step-by-step path description
- Final coin count
- Total amount stolen

## Future Objectives

The project will be expanded to include:

1. Objective 2: Finding the path with maximum possible profit
2. Objective 3: Finding the path with minimum possible loss to thieves

## Technical Requirements

- Python 3.x
- Standard library modules: collections, sys

## Usage

Run the program and provide input in the specified format:

```bash
python main.py
```

## Notes

- The implementation handles edge cases and input validation
- Negative coin values are allowed
- Start and end cells are considered part of the grid and may contain any type of cell
