import collections
import sys
import heapq  # For the priority queue

# Increase recursion depth (might not be needed for iterative searches)
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
    elif isinstance(start_val, int):
        current_coins += start_val

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

        value_str = str(cell_value) if cell_value != "!" else "!"
        path_description.append(f"{move} ({value_str})")

        # --- Apply Thief/Coin Logic ---
        if with_thief:
            if cell_value == "!":
                with_thief = False
            elif isinstance(cell_value, int):
                if cell_value > 0:
                    total_stolen += cell_value
                else:
                    total_stolen += abs(cell_value)
                with_thief = False
        else:
            if cell_value == "!":
                with_thief = True
            elif isinstance(cell_value, int):
                current_coins += cell_value

    return current_coins, total_stolen, path_description


# --- Helper Function to Precompute an Optimistic Heuristic ---
def compute_future_max(n, grid):
    """
    Compute an optimistic maximum coins reachable from each cell to the destination,
    ignoring thief-related effects (treating thief cells as 0).
    Allowed moves: Down and Right.
    """
    dp = [[-float("inf")] * n for _ in range(n)]
    for r in range(n - 1, -1, -1):
        for c in range(n - 1, -1, -1):
            # For heuristic purposes, treat "!" as 0 coin contribution.
            cell_val = grid[r][c] if grid[r][c] != "!" else 0
            if r == n - 1 and c == n - 1:
                dp[r][c] = cell_val
            else:
                best_next = -float("inf")
                if r + 1 < n:
                    best_next = max(best_next, dp[r + 1][c])
                if c + 1 < n:
                    best_next = max(best_next, dp[r][c + 1])
                dp[r][c] = cell_val + best_next
    return dp


# --- Objective 2 Implementation with Informed Search (A*) ---
def solve_objective2_informed(n, grid):
    """
    Finds the path that maximizes the final coin count using an informed A* search,
    based on the provided project phase "بیشترین سود ممکن".
    """
    print("--- Objective 2: Maximize Final Coins (Informed A* Search) ---")
    future_max = compute_future_max(n, grid)
    start_node = (0, 0)
    end_node = (n - 1, n - 1)

    # Initial State: (row, col, has_thief)
    start_val = grid[0][0]
    initial_coins = 0
    initial_thief = False
    if start_val == "!":
        initial_thief = True
    elif isinstance(start_val, int):
        initial_coins = start_val

    initial_state = (0, 0, initial_thief)
    # Priority Queue stores: (f, coins_so_far, row, col, thief_status, path_list)
    # f = -(coins_so_far + future_max[r][c])
    pq = []
    initial_f = -(initial_coins + future_max[0][0])
    heapq.heappush(pq, (initial_f, initial_coins, 0, 0, initial_thief, [start_node]))

    # Dictionary to record the best coin count obtained for a given state:
    best_state = {}
    best_path = None
    best_coins = -float("inf")

    while pq:
        f, coins, r, c, thief, path = heapq.heappop(pq)
        state = (r, c, thief)
        if coins < best_state.get(state, -float("inf")):
            continue  # We already found a better way to this state

        # Goal check: reached destination
        if (r, c) == end_node:
            if coins > best_coins:
                best_coins = coins
                best_path = path

        # Expand Neighbors (Down and Right moves):
        for move, nr, nc in [("Down", r + 1, c), ("Right", r, c + 1)]:
            if nr < n and nc < n:
                neighbor_value = grid[nr][nc]
                new_coins = coins
                new_thief = thief
                # Transition logic according to thief/coin rules:
                if thief:  # Arriving with a thief in the car:
                    if neighbor_value == "!":
                        new_thief = False  # Thief fight, thief leaves; coins unchanged.
                    elif isinstance(neighbor_value, int):
                        new_thief = (
                            False  # Thief steals the coin value; coins remain the same.
                        )
                else:  # No thief in the car:
                    if neighbor_value == "!":
                        new_thief = True  # Pick up thief.
                    elif isinstance(neighbor_value, int):
                        new_coins += neighbor_value  # Add coin value.
                        new_thief = False
                new_state = (nr, nc, new_thief)
                if new_coins > best_state.get(new_state, -float("inf")):
                    best_state[new_state] = new_coins
                    new_path = path + [(nr, nc)]
                    # f = -(new_coins + heuristic from neighbor)
                    new_f = -(new_coins + future_max[nr][nc])
                    heapq.heappush(pq, (new_f, new_coins, nr, nc, new_thief, new_path))

    if best_path:
        # Recalculate the final outcome for the best path found using full simulation.
        final_coins, total_stolen, path_desc = calculate_path_outcome(
            n, grid, best_path
        )
        print("Best Path Found for Maximum Coins (Informed):")
        for i, step in enumerate(path_desc):
            print(f"{i + 1}. {step}")
        print(f"\nFinal Coins: {final_coins}")
        print(f"Total Stolen: {total_stolen}")
    else:
        print("No path found to the destination.")
    print("-" * 20)


if __name__ == "__main__":
    n_size, grid_data = parse_input()

    # --- (Informed A* Search for maximizing coins) ---
    solve_objective2_informed(n_size, grid_data)
