import numpy as np

THIEF_MARKER_INTERNAL = float('inf') # مقدار داخلی برای نمایش دزد

def load_map(file_path):
    """نقشه را از فایل متنی می‌خواند و به آرایه NumPy تبدیل می‌کند."""
    map_data = []
    with open(file_path, 'r') as f:
        for line in f:
            row = []
            items = line.strip().split()
            if not items: continue # Skip empty lines
            for item in items:
                try:
                    val = int(item)
                    row.append(val)
                except ValueError:
                    if item == '!':
                        row.append(THIEF_MARKER_INTERNAL)
                    else:
                        raise ValueError(f"Invalid item in map: {item}")
            map_data.append(row)

    if not map_data:
        raise ValueError("Map is empty!")

    n = len(map_data)
    for r in map_data:
        if len(r) != n:
            raise ValueError(f"Map is not square!")

    return np.array(map_data, dtype=float), n # Use float for infinity marker