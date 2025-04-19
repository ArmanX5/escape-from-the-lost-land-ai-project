# Escape from the Lost Land - AI Project

An artificial intelligence project implementing pathfinding algorithms to solve a grid-based escape scenario with multiple objectives.

## Contributors

**Arman Akhoundy** ([ArmanX5](https://github.com/ArmanX5)) & **Amirreza Abbasian** ([Amirreza0924](https://github.com/Amirreza0924))

## Project Overview

The project implements three different pathfinding approaches in a game where a character named Arian must navigate through a grid containing treasures and thieves. Each phase tackles a different objective:

1. Phase 1: Find a valid path using BFS
2. Phase 2: Find the path maximizing profit using A*
3. Phase 3: Find the path minimizing thief losses using A*

## Game Rules

- Grid is n×n with movement restricted to Down and Right
- Cell types:
  - Normal: Negative numbers (costs)
  - Treasure: Positive numbers (coins)
  - Thief: Marked with "!"
- Thief mechanics:
  - Thieves join Arian until next cell
  - They steal treasures or costs and leave
  - Two thieves fight each other and leave
  - Thieves return to original positions after leaving

## Project Structure

```
├── Phase 1/         # Basic pathfinding (BFS)
├── Phase 2/         # Maximum profit path (A*)
└── Phase-3/         # Minimum loss path (A*)
```

## Usage

Run any phase:
```bash
cd Phase-N  # N = 1, 2, or 3
python main.py < map.txt
```

Input format:
```
n
a11 a12 ... a1n
a21 a22 ... a2n
...
an1 an2 ... ann
```

Requirements:
- Python 3.x
- NumPy (for Phase 3)

For detailed documentation of each phase, see:
- Phase 1: `Phase 1/phase-1.md`
- Phase 2: `Phase 2/phase-2.md`
- Phase 3: `Phase-3/README.md`
