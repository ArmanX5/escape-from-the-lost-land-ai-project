import heapq
import numpy as np
from utils import Node, reconstruct_path_nodes, calculate_final_stats
from map_loader import THIEF_MARKER_INTERNAL

def solve_scenario3_astar(game_map, n):
    """سناریوی 3 (کمترین زیان) را با A* حل می‌کند."""
    start_r, start_c = 0, 0
    goal_r, goal_c = n - 1, n - 1

    # تابع هیوریستیک (h=0 : خوش‌بینانه برای کمینه کردن زیان)
    def heuristic(r, c, has_thief):
        return 0

    # تعیین وضعیت اولیه (دزد در خانه شروع؟)
    initial_cell_value = game_map[start_r, start_c]
    initial_has_thief = (initial_cell_value == THIEF_MARKER_INTERNAL)
    initial_g_cost = 0 # زیان اولیه صفر است

    start_node = Node(start_r, start_c, initial_has_thief,
                      g_cost=initial_g_cost,
                      h_cost=heuristic(start_r, start_c, initial_has_thief))

    open_set = []  # صف اولویت (min-heap)
    heapq.heappush(open_set, start_node)

    # مجموعه یا دیکشنری برای نودهای بازدید شده و هزینه رسیدن به آن‌ها
    # key: (r, c, has_thief), value: g_cost
    visited = {}
    visited[(start_node.r, start_node.c, start_node.has_thief)] = start_node.g_cost

    while open_set:
        current_node = heapq.heappop(open_set)

        # بررسی رسیدن به هدف
        if current_node.r == goal_r and current_node.c == goal_c:
            path_nodes = reconstruct_path_nodes(current_node)
            final_coins, total_stolen = calculate_final_stats(path_nodes, game_map)
            final_path_coords = [(node.r, node.c) for node in path_nodes]
            return final_path_coords, final_coins, total_stolen # مسیر پیدا شد

        # تولید جانشین‌ها (حرکت به پایین و راست)
        for move in [(1, 0), (0, 1)]: # پایین, راست
            next_r, next_c = current_node.r + move[0], current_node.c + move[1]

            # بررسی معتبر بودن مختصات
            if 0 <= next_r < n and 0 <= next_c < n:
                next_cell_value = game_map[next_r, next_c]
                step_loss = 0 # زیان این حرکت خاص
                next_has_thief = False # وضعیت دزد *بعد از* ورود به خانه بعدی

                # محاسبه زیان و وضعیت دزد بعدی
                if current_node.has_thief: # اگر دزد از خانه فعلی همراه بود
                    if next_cell_value == THIEF_MARKER_INTERNAL:
                        step_loss = 0
                        next_has_thief = False # دعوا شد، دزد فعلی رفت
                    elif next_cell_value > 0: # گنجینه
                        step_loss = next_cell_value
                        next_has_thief = False # دزد گنج را برد و رفت
                    else: # عادی (منفی)
                        step_loss = abs(next_cell_value)
                        next_has_thief = False # دزد پول را گرفت و رفت
                else: # دزدی همراه نبود
                    step_loss = 0
                    if next_cell_value == THIEF_MARKER_INTERNAL:
                        next_has_thief = True # دزد جدید سوار شد
                    else:
                        next_has_thief = False # همچنان بدون دزد

                # محاسبه هزینه‌های نود جانشین
                new_g_cost = current_node.g_cost + step_loss
                new_h_cost = heuristic(next_r, next_c, next_has_thief)
                successor_node = Node(next_r, next_c, next_has_thief,
                                    g_cost=new_g_cost, h_cost=new_h_cost,
                                    parent=current_node)

                # بررسی وضعیت در مجموعه visited
                successor_state = (successor_node.r, successor_node.c, successor_node.has_thief)
                if successor_state not in visited or new_g_cost < visited[successor_state]:
                    visited[successor_state] = new_g_cost
                    heapq.heappush(open_set, successor_node)

    return None, 0, 0 # مسیر پیدا نشد