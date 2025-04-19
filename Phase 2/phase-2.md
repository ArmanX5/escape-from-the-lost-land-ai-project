# Escape from the Lost Land - Phase 2 Documentation

## Phase 2 Overview

Phase 2 of the project implements the second objective: finding the path that maximizes the final coin count for Arian. This phase uses an informed search algorithm (A\*) to find the optimal path that yields the highest possible profit.

## Implementation Details

### Key Components

1. `parse_input()`: Reads and validates the grid configuration from standard input
2. `calculate_path_outcome()`: Helper function that calculates the final coins and stolen amount for a given path
3. `compute_future_max()`: Computes an optimistic heuristic for the A\* algorithm
4. `solve_objective2_informed()`: Implements the A\* search algorithm to find the path with maximum profit

### Algorithm Details

The implementation uses an A\* search algorithm with the following characteristics:

#### State Representation

- Each state is represented as a tuple: (row, column, has_thief)
- The algorithm tracks:
  - Current position (row, column)
  - Current coin count
  - Whether a thief is currently in the vehicle

#### Heuristic Function

- Uses an optimistic heuristic that precomputes the maximum possible coins reachable from each cell to the destination
- The heuristic ignores thief-related effects (treating thief cells as 0)
- This provides an admissible and consistent heuristic for the A\* algorithm

#### Priority Queue

- The priority queue stores tuples: (f, coins_so_far, row, col, thief_status, path_list)
- f = -(coins_so_far + future_max[r][c])
- Lower f values have higher priority (using negative values to maximize profit)

#### State Tracking

- Maintains a dictionary to record the best coin count obtained for each state
- Prunes states that have already been visited with a better coin count

### Thief and Coin Logic

The algorithm handles the following scenarios:

1. When encountering a thief:
   - If no thief is in the vehicle: Pick up the thief
   - If a thief is already in the vehicle: Thieves fight and leave
2. When moving to a cell with coins:
   - If no thief is in the vehicle: Add coins to the total
   - If a thief is in the vehicle: Thief steals the coins and leaves

## Input/Output Format

### Input Format

Same as Phase 1:

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

### Output Format

The output includes:

1. A header indicating this is Objective 2 (Maximize Final Coins)
2. The complete path from start to end with each move (Down/Right) and cell value
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
- Final coin count (maximized)
- Total amount stolen

## Technical Requirements

- Python 3.x
- Standard library modules: sys, heapq

## Usage

Run the program and provide input in the specified format:

```bash
python main.py
```

## Algorithm Complexity

- Time Complexity: O(n² \* 2) where n is the grid size and 2 represents the binary state of having a thief or not
- Space Complexity: O(n²) for the heuristic table and state tracking

## Notes

- The A\* algorithm guarantees finding the optimal path when using an admissible heuristic
- The implementation handles all edge cases including:
  - Multiple thieves
  - Negative coin values
  - Start and end cells with special properties
- The optimistic heuristic ensures the algorithm will find the globally optimal solution
