import collections
import sys

# Increase recursion depth for potentially deep paths, though BFS isn't recursive
# sys.setrecursionlimit(2000) # Usually not needed for iterative BFS


def parse_input():
    """Reads the grid configuration from standard input."""
    try:
        n = int(sys.stdin.readline().strip())
        if n <= 0:
            raise ValueError("Grid size must be positive.")
        grid_repr = [sys.stdin.readline().split() for _ in range(n)]

        grid = []
        for r in range(n):
            row_data = []
            if len(grid_repr[r]) != n:
                raise ValueError(f"Row {r} does not have {n} elements.")
            for cell_repr in grid_repr[r]:
                if cell_repr == "!":
                    row_data.append("!")
                else:
                    try:
                        row_data.append(int(cell_repr))
                    except ValueError:
                        raise ValueError(f"Invalid cell value: {cell_repr}")
            grid.append(row_data)
        return n, grid
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)


def solve_objective1(n, grid):
    """
    Finds a path from (0, 0) to (n-1, n-1) using BFS.
    The search itself ignores costs/thieves, just finds reachability.
    Then, calculates the outcome for the found path.
    """
    start_node = (0, 0)
    end_node = (n - 1, n - 1)

    # Queue stores tuples: ( (row, col), path_list_of_coords )
    queue = collections.deque([(start_node, [start_node])])
    visited = {start_node}

    path_found = None

    while queue:
        (r, c), path_coords = queue.popleft()

        # Goal check
        if (r, c) == end_node:
            path_found = path_coords
            break

        # Explore neighbors (Down, Right)
        moves = [("Down", r + 1, c), ("Right", r, c + 1)]

        for move_name, nr, nc in moves:
            # Check boundaries
            if 0 <= nr < n and 0 <= nc < n:
                neighbor_coord = (nr, nc)
                # Check if visited
                if neighbor_coord not in visited:
                    visited.add(neighbor_coord)
                    new_path_coords = path_coords + [neighbor_coord]
                    queue.append((neighbor_coord, new_path_coords))

    # --- Path Found - Now Calculate Outcome and Format Output ---
    if path_found:
        print("Path for Objective 1 (BFS - First Found Path):")

        current_coins = 0
        total_stolen = 0
        with_thief = False
        path_description = []

        # Process start cell (0, 0)
        start_val = grid[0][0]
        if start_val == "!":
            with_thief = True
            # print(f"Debug: Start at (0,0), picked up thief.")
        elif isinstance(start_val, int):
            current_coins += start_val
            # print(f"Debug: Start at (0,0), value {start_val}, coins={current_coins}")

        # Process the rest of the path
        for i in range(1, len(path_found)):
            prev_r, prev_c = path_found[i - 1]
            curr_r, curr_c = path_found[i]
            cell_value = grid[curr_r][curr_c]

            move = ""
            if curr_r > prev_r:
                move = "Down"
            elif curr_c > prev_c:
                move = "Right"

            # Format cell value for description, handle '!'
            value_str = str(cell_value) if cell_value != "!" else "!"
            path_description.append(f"{move} ({value_str})")
            # print(f"Debug: Moved {move} to ({curr_r},{curr_c}), value={cell_value}, thief_present={with_thief}")

            # --- Apply Thief/Coin Logic ---
            if with_thief:
                if cell_value == "!":
                    # Thief fight! Thief leaves.
                    with_thief = False
                    # print(f"Debug: Thief fight at ({curr_r},{curr_c}), thief leaves.")
                elif isinstance(cell_value, int):
                    if cell_value > 0:  # Treasure cell
                        total_stolen += cell_value
                        # print(f"Debug: Thief steals {cell_value} treasure at ({curr_r},{curr_c}). Stolen={total_stolen}")
                    else:  # Normal cell (cost <= 0)
                        # Cost is negative, amount stolen is positive abs(value)
                        total_stolen += abs(cell_value)
                        # print(f"Debug: Thief steals {-cell_value} cost at ({curr_r},{curr_c}). Stolen={total_stolen}")
                    # Thief always leaves after stealing or encountering a non-thief cell
                    with_thief = False
                    # print(f"Debug: Thief leaves after action at ({curr_r},{curr_c}).")

            else:  # Not currently with a thief
                if cell_value == "!":
                    # Pick up a new thief
                    with_thief = True
                    # print(f"Debug: Picked up thief at ({curr_r},{curr_c}).")
                elif isinstance(cell_value, int):
                    # Add treasure or apply cost
                    current_coins += cell_value
                    # print(f"Debug: Applied value {cell_value} at ({curr_r},{curr_c}). Coins={current_coins}")

        # Print the formatted path description
        for i, step in enumerate(path_description):
            print(f"{i+1}. {step}")

        # Print the final results
        print(f"\nFinal Coins: {current_coins}")
        print(f"Total Stolen: {total_stolen}")

    else:
        print("Objective 1: No path found from start to end.")


if __name__ == "__main__":
    n_size, grid_data = parse_input()
    solve_objective1(n_size, grid_data)
