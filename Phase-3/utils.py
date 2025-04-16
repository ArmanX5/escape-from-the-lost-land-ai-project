import numpy as np
from map_loader import THIEF_MARKER_INTERNAL

class Node:
    """نمایش یک حالت در فضای جستجو (موقعیت + وضعیت دزد)."""
    def __init__(self, r, c, has_thief, g_cost=0, h_cost=0, parent=None):
        self.r = r
        self.c = c
        self.has_thief = has_thief # Boolean: آیا دزدی همراه آریان هست؟
        self.g_cost = g_cost # هزینه انباشته (زیان دزدیده شده) تا این نود
        self.h_cost = h_cost # هزینه هیوریستیک (زیان تخمینی آینده)
        self.parent = parent # برای بازسازی مسیر

    @property
    def f_cost(self):
        """هزینه کل تخمینی (f = g + h)."""
        return self.g_cost + self.h_cost

    # لازم برای مقایسه نودها در صف اولویت (heapq)
    def __lt__(self, other):
        # اولویت با f_cost کمتر
        return self.f_cost < other.f_cost

    # لازم برای ذخیره در مجموعه visited (set)
    def __eq__(self, other):
        return isinstance(other, Node) and self.r == other.r and self.c == other.c and self.has_thief == other.has_thief

    def __hash__(self):
        return hash((self.r, self.c, self.has_thief))

    def __repr__(self):
         return f"Node(r={self.r}, c={self.c}, thief={self.has_thief}, g={self.g_cost}, h={self.h_cost})"


def reconstruct_path_nodes(node):
    """مسیر را به صورت لیستی از نودها از شروع به پایان بازسازی می‌کند."""
    nodes = []
    current = node
    while current:
        nodes.append(current)
        current = current.parent
    return nodes[::-1]

def calculate_final_stats(path_nodes, game_map):
    """محاسبه سکه نهایی آریان و کل زیان دزدیده شده بر اساس مسیر نودها."""
    coins = 0
    stolen = 0
    n = game_map.shape[0]

    if not path_nodes:
        return 0, 0

    # وضعیت اولیه در خانه (0,0)
    start_node = path_nodes[0]
    start_r, start_c = start_node.r, start_node.c
    start_cell_value = game_map[start_r, start_c]

    # وضعیت دزد *بعد از* اعمال اثر خانه شروع
    current_has_thief = start_node.has_thief

    # اعمال اثر خود خانه شروع بر سکه‌های آریان (این جزو زیان محاسبه نمی‌شود)
    if start_cell_value != THIEF_MARKER_INTERNAL:
        if start_cell_value > 0:
            coins += start_cell_value # گنجینه اولیه
        else: # شامل هزینه عادی < 0
            coins += start_cell_value # هزینه اولیه

    # پیمایش حرکت‌ها بین نودها
    for i in range(len(path_nodes) - 1):
        current_node = path_nodes[i] # نود فعلی (از آن حرکت می‌کنیم)
        next_node = path_nodes[i+1]   # نود بعدی (به آن می‌رسیم)
        next_r, next_c = next_node.r, next_node.c
        next_cell_value = game_map[next_r, next_c]

        # دزدی که از خانه current_node سوار شده (اگر شده باشد) در خانه next_node عمل می‌کند
        thief_was_present_before_move = current_node.has_thief
        step_loss = 0
        arian_gain_loss = 0 # تغییر مستقیم سکه آریان در این مرحله

        if thief_was_present_before_move:
            if next_cell_value == THIEF_MARKER_INTERNAL:
                step_loss = 0 # دعوا
            elif next_cell_value > 0: # گنجینه
                step_loss = next_cell_value
            elif next_cell_value < 0: # عادی
                step_loss = abs(next_cell_value)
            # دزد در هر صورت پیاده می‌شود (یا بخاطر دعوا یا بعد از دزدی)
        else:
            # دزدی همراه نبود، آریان خودش با خانه بعدی تعامل می‌کند
            step_loss = 0
            if next_cell_value != THIEF_MARKER_INTERNAL:
                arian_gain_loss = next_cell_value # گنجینه یا هزینه عادی

        stolen += step_loss
        coins += arian_gain_loss

        # وضعیت دزد برای مرحله بعد، همان وضعیت ذخیره شده در نود بعدی است
        current_has_thief = next_node.has_thief

    return int(coins), int(stolen)