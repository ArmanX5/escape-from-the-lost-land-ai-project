from map_loader import load_map
from a_star_solver import solve_scenario3_astar
from pathlib import Path

def main():
    map_file = Path("Phase-3", "map2.txt")
    try:
        game_map, n = load_map(map_file)
        print(f"Map {n}x{n} loaded from file '{map_file}'.")
        print("-" * 30)

        print("Solving scenario 3 (minimum loss) with A*...")
        path3, coins3, stolen3 = solve_scenario3_astar(game_map, n)

        if path3:
            print("\n--- Results of Scenario 3 ---")
            print(f"Path: {path3}")
            print(f"Coins collected by Aryan: {coins3}")
            print(f"Total stolen coins (minimized): {stolen3}")
        else:
            print("\n--- Results of Scenario 3 ---")
            print("No path found for scenario 3.")

    except FileNotFoundError:
        print(f"Error: Map file '{map_file}' not found.")
    except ValueError as e:
        print(f"Error processing map: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()