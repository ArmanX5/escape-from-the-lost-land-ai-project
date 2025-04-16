import collections
import sys
import heapq  # For the priority queue

# Increase recursion depth (might not be needed for iterative Dijkstra, but safe)
# sys.setrecursionlimit(2000)


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


# --- Helper Function to Calculate Path Outcome (Reused for all objectives) ---
def calculate_path_outcome(n, grid, path_coords):
    """
    Calculates final coins and stolen amount for a given path.
    Returns: (final_coins, total_stolen, path_description_list)
    """
    if not path_coords:
        return 0, 0, []

    current_coins = 0
    total_stolen = 0
    with_thief = False
    path_description = []

    # Process start cell (0, 0)
    start_r, start_c = path_coords[0]
    start_val = grid[start_r][start_c]

    if start_val == "!":
        with_thief = True
        # print(f"Debug: Start at (0,0), picked up thief.") # Optional debug
    elif isinstance(start_val, int):
        current_coins += start_val
        # print(f"Debug: Start at (0,0), value {start_val}, coins={current_coins}") # Optional debug

    # Process the rest of the path
    for i in range(1, len(path_coords)):
        prev_r, prev_c = path_coords[i - 1]
        curr_r, curr_c = path_coords[i]
        cell_value = grid[curr_r][curr_c]

        move = ""
        if curr_r > prev_r:
            move = "Down"
        elif curr_c > prev_c:
            move = "Right"

        # Format cell value for description
        value_str = str(cell_value) if cell_value != "!" else "!"
        path_description.append(f"{move} ({value_str})")
        # print(f"Debug: Moved {move} to ({curr_r},{curr_c}), value={value_str}, thief_present={with_thief}") # Optional debug

        # --- Apply Thief/Coin Logic ---
        if with_thief:
            # Thief was already in the car when arriving at (curr_r, curr_c)
            if cell_value == "!":
                # Thief fight! Thief leaves. No coin change for this step.
                with_thief = False
                # print(f"Debug: Thief fight at ({curr_r},{curr_c}), thief leaves.") # Optional debug
            elif isinstance(cell_value, int):
                # Thief acts (steals) and leaves.
                if cell_value > 0:  # Treasure cell
                    total_stolen += cell_value
                    # print(f"Debug: Thief steals {cell_value} treasure at ({curr_r},{curr_c}). Stolen={total_stolen}") # Optional debug
                else:  # Normal cell (cost <= 0)
                    total_stolen += abs(
                        cell_value
                    )  # Steals the equivalent positive amount
                    # print(f"Debug: Thief steals {-cell_value} cost at ({curr_r},{curr_c}). Stolen={total_stolen}") # Optional debug
                # Thief always leaves after acting on a non-thief cell
                with_thief = False
                # print(f"Debug: Thief leaves after action at ({curr_r},{curr_c}).") # Optional debug
        else:
            # No thief in the car when arriving at (curr_r, curr_c)
            if cell_value == "!":
                # Pick up a new thief
                with_thief = True
                # print(f"Debug: Picked up thief at ({curr_r},{curr_c}).") # Optional debug
            elif isinstance(cell_value, int):
                # Add treasure or apply cost normally
                current_coins += cell_value
                # print(f"Debug: Applied value {cell_value} at ({curr_r},{curr_c}). Coins={current_coins}") # Optional debug

    return current_coins, total_stolen, path_description


# --- Objective 1 Implementation (Uninformed BFS - for comparison/completeness) ---
def solve_objective1(n, grid):
    """
    Finds *a* path using BFS (ignores costs/thieves during search).
    Then calculates the outcome for that specific path.
    """
    print("--- Objective 1: Just Reach the End (BFS) ---")
    start_node = (0, 0)
    end_node = (n - 1, n - 1)

    queue = collections.deque([(start_node, [start_node])])  # (coord, path_list)
    visited = {start_node}
    found_path_coords = None

    while queue:
        (r, c), path_coords = queue.popleft()

        if (r, c) == end_node:
            found_path_coords = path_coords
            break

        moves = [("Down", r + 1, c), ("Right", r, c + 1)]
        for move_name, nr, nc in moves:
            if 0 <= nr < n and 0 <= nc < n:
                neighbor_coord = (nr, nc)
                if neighbor_coord not in visited:
                    visited.add(neighbor_coord)
                    new_path_coords = path_coords + [neighbor_coord]
                    queue.append((neighbor_coord, new_path_coords))

    if found_path_coords:
        final_coins, total_stolen, path_desc = calculate_path_outcome(
            n, grid, found_path_coords
        )

        print("Path Found:")
        for i, step in enumerate(path_desc):
            print(f"{i + 1}. {step}")
        print(f"\nFinal Coins: {final_coins}")
        print(f"Total Stolen: {total_stolen}")
    else:
        print("No path found.")
    print("-" * 20)


# --- Objective 2 Implementation (Maximize Coins - Dijkstra Adaptation) ---
def solve_objective2(n, grid):
    """
    Finds the path that maximizes the final coin count using Dijkstra's algorithm
    adapted for maximization and state (with_thief).
    """
    print("--- Objective 2: Maximize Final Coins ---")
    start_node = (0, 0)
    end_node = (n - 1, n - 1)

    # State: (row, col, has_thief_currently)
    # Priority Queue stores: (-current_coins, r, c, has_thief, path_list)
    # We use -current_coins because heapq is a min-heap, achieving max-heap behavior.
    pq = []
    # Keep track of max coins found *so far* for reaching a specific state (r, c, has_thief)
    # Initialize with negative infinity
    max_coins_at_state = collections.defaultdict(lambda: -float("inf"))

    # --- Initial State ---
    start_r, start_c = start_node
    start_val = grid[start_r][start_c]
    initial_coins = 0
    initial_thief = False

    if start_val == "!":
        initial_thief = True
    elif isinstance(start_val, int):
        initial_coins = start_val  # Start collecting/paying from the first cell

    initial_state = (start_r, start_c, initial_thief)
    initial_path = [start_node]
    max_coins_at_state[initial_state] = initial_coins
    heapq.heappush(pq, (-initial_coins, start_r, start_c, initial_thief, initial_path))

    best_path_to_dest = None
    max_final_coins = -float(
        "inf"
    )  # Track the best outcome *found* for any path ending at the destination

    # --- Dijkstra's Search ---
    while pq:
        neg_coins, r, c, current_thief_status, path = heapq.heappop(pq)
        current_coins = -neg_coins

        # Optimization: If we found a better way to reach this state already, skip
        if current_coins < max_coins_at_state.get(
            (r, c, current_thief_status), -float("inf")
        ):
            continue

        # --- Goal Check ---
        # We check if we've reached the *destination coordinates*. The final coin calculation
        # will happen *after* the full path is determined.
        if (r, c) == end_node:
            # Calculate the actual final outcome for *this specific path*
            # We need to simulate this path to get the true end coins and stolen amount
            path_final_coins, path_total_stolen, _ = calculate_path_outcome(
                n, grid, path
            )

            # Update the overall best path found if this one yields more final coins
            if path_final_coins > max_final_coins:
                max_final_coins = path_final_coins
                best_path_to_dest = path
            # Continue searching, another path might reach the end state (r,c,thief_status)
            # later but result in an even better final coin count after simulation.

        # --- Explore Neighbors (Down, Right) ---
        moves = [("Down", r + 1, c), ("Right", r, c + 1)]
        for move_name, nr, nc in moves:
            # Check boundaries
            if 0 <= nr < n and 0 <= nc < n:
                neighbor_coord = (nr, nc)
                neighbor_value = grid[nr][nc]
                next_coins = current_coins  # Coins *before* processing neighbor cell
                next_thief_status = current_thief_status

                # --- Determine state *after* moving to (nr, nc) ---
                # This logic determines the state for the *next* node in the search graph
                # It mirrors the path simulation logic but applies it prospectively

                temp_stolen_in_step = (
                    0  # Not directly used for priority, but helps clarity
                )

                if current_thief_status:  # Arriving at (nr, nc) with a thief
                    if neighbor_value == "!":
                        # Thief fight, thief leaves for the *next* state
                        next_thief_status = False
                        # Coins don't change in this step
                    elif isinstance(neighbor_value, int):
                        # Thief acts and leaves for the *next* state
                        next_thief_status = False
                        # Coin state for next node is unaffected by theft in *this* step
                        # (Theft affects final calculation, not search priority)
                        if neighbor_value > 0:
                            temp_stolen_in_step = neighbor_value
                        else:
                            temp_stolen_in_step = abs(neighbor_value)
                else:  # Arriving at (nr, nc) without a thief
                    if neighbor_value == "!":
                        # Pick up thief for the *next* state
                        next_thief_status = True
                        # Coins don't change in this step
                    elif isinstance(neighbor_value, int):
                        # Apply value normally, no thief for the *next* state
                        next_thief_status = False
                        next_coins += (
                            neighbor_value  # Update coin count for the next state
                        )

                # --- Check if this path to the neighbor state is better ---
                neighbor_state = (nr, nc, next_thief_status)
                if next_coins > max_coins_at_state.get(neighbor_state, -float("inf")):
                    max_coins_at_state[neighbor_state] = next_coins
                    new_path = path + [neighbor_coord]
                    heapq.heappush(
                        pq, (-next_coins, nr, nc, next_thief_status, new_path)
                    )

    # --- Output Results for Objective 2 ---
    if best_path_to_dest:
        # Recalculate the outcome for the definitively best path found
        final_coins, total_stolen, path_desc = calculate_path_outcome(
            n, grid, best_path_to_dest
        )

        print("Best Path Found for Maximum Coins:")
        # Optional: Print the coordinates if needed
        # print("Coordinates:", best_path_to_dest)
        for i, step in enumerate(path_desc):
            print(f"{i + 1}. {step}")
        print(f"\nFinal Coins: {final_coins}")  # Should match max_final_coins
        print(f"Total Stolen: {total_stolen}")
    else:
        # This should generally not happen if a path exists,
        # unless all paths result in -infinity coins (highly unlikely)
        print("No path found to the destination.")
    print("-" * 20)


if __name__ == "__main__":
    n_size, grid_data = parse_input()

    # --- Solve Objective 1 (Example) ---
    # solve_objective1(n_size, grid_data) # You can uncomment this if needed

    # --- Solve Objective 2 ---
    solve_objective2(n_size, grid_data)

    # --- Placeholder for Objective 3 ---
    # solve_objective3(n_size, grid_data)
