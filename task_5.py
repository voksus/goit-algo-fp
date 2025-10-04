# Очистка консолі (залишено з вашого прикладу)
print('\033c', end='')

import uuid
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# --- КОНСТАНТИ ТА НАЛАШТУВАННЯ ---

# Кольори для візуалізації обходу (градієнт від темного до світлого)
INITIAL_COLOR = '#BBBBBB'
COLORS = [
    "#1565C0",  # Темний синій
    "#1976D2",
    "#1E88E5",
    "#2196F3",  # Класичний синій
    "#42A5F5",
    "#64B5F6",
    "#90CAF9",  # Світлий блакитний
]
PAUSE_DURATION = 0.4  # Тривалість паузи між кроками в секундах

# Налаштування кнопки "Продовжити"
BUTTON_POS_X  = 0.65
BUTTON_POS_Y  = 0.02
BUTTON_WIDTH  = 0.3
BUTTON_HEIGHT = 0.06
BUTTON_TEXT   = 'Продовжити (до BFS)'
BUTTON_TEXT_COLOR = '#0D47A1'
BUTTON_BG_COLOR   = '#90CAF9'
BUTTON_HV_COOR    = '#BBDEFB'

# --- ЛОГІКА КНОПКИ ТА ГЛОБАЛЬНІ ЗМІННІ ---

PROCEED_FLAG    : bool     = False
BUTTON_INSTANCE : Button   = None
BUTTON_AXES     : plt.Axes = None

def on_button_click(event):
    """Обробник події натискання на кнопку."""
    global PROCEED_FLAG, BUTTON_INSTANCE, BUTTON_AXES
    PROCEED_FLAG = True
    if BUTTON_INSTANCE:
        BUTTON_INSTANCE.disconnect_events()
    if BUTTON_AXES:
        BUTTON_AXES.remove()
        plt.draw()

def wait_for_button_click(fig: plt.Figure):
    """Створює кнопку і блокує виконання до її натискання."""
    global PROCEED_FLAG, BUTTON_INSTANCE, BUTTON_AXES
    PROCEED_FLAG = False

    BUTTON_AXES = fig.add_axes([BUTTON_POS_X, BUTTON_POS_Y, BUTTON_WIDTH, BUTTON_HEIGHT])
    BUTTON_INSTANCE = Button(BUTTON_AXES, BUTTON_TEXT, color=BUTTON_BG_COLOR, hovercolor=BUTTON_HV_COOR)
    BUTTON_INSTANCE.label.set_fontsize(14)
    BUTTON_INSTANCE.label.set_fontweight(500)
    BUTTON_INSTANCE.label.set_color(BUTTON_TEXT_COLOR)
    BUTTON_INSTANCE.on_clicked(on_button_click)

    plt.draw()

    # Цикл очікування, доки прапорець не стане True
    while not PROCEED_FLAG:
        plt.pause(0.1)

# --- КЛАС ВУЗЛА ТА ФУНКЦІЇ ВІДОБРАЖЕННЯ ДЕРЕВА ---

class Node:
    def __init__(self, key, color=INITIAL_COLOR):
        self.left  : Node = None
        self.right : Node = None
        self.val   = key
        self.color = color
        self.id    = str(uuid.uuid4())

def add_edges(graph: nx.DiGraph, node: Node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def _draw_tree_on_ax(ax: plt.Axes, tree_root: Node):
    """Допоміжна функція для перемальовування дерева на існуючому полотні."""
    ax.clear()
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors, ax=ax)
    plt.draw()


# --- ФУНКЦІЇ АЛГОРИТМІВ ОБХОДУ ТА ВІЗУАЛІЗАЦІЇ ---

def reset_node_colors(node: Node):
    """Рекурсивно скидає колір всіх вузлів до початкового."""
    if node:
        node.color = INITIAL_COLOR
        reset_node_colors(node.left)
        reset_node_colors(node.right)

def visualize_dfs(root: Node, ax: plt.Axes):
    """Візуалізує обхід дерева в глибину (DFS)."""
    ax.set_title("Обхід дерева вглибину (DFS)")
    visited = set()
    stack = [root]
    color_index = 0

    while stack:
        node = stack.pop()
        if node and node not in visited:
            visited.add(node)
            node.color = COLORS[color_index % len(COLORS)]
            color_index += 1

            _draw_tree_on_ax(ax, root)
            ax.set_title("Обхід дерева вглибину (DFS)")
            plt.pause(PAUSE_DURATION)

            # Додаємо правий, а потім лівий, щоб лівий оброблявся першим
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

def visualize_bfs(root: Node, ax: plt.Axes):
    """Візуалізує обхід дерева в ширину (BFS)."""
    ax.set_title("Обхід дерева вширину (BFS)")
    visited = {root}
    queue = deque([root])
    color_index = 0

    while queue:
        node = queue.popleft()
        node.color = COLORS[color_index % len(COLORS)]
        color_index += 1

        _draw_tree_on_ax(ax, root)
        ax.set_title("Обхід дерева вширину (BFS)")
        plt.pause(PAUSE_DURATION)

        if node.left and node.left not in visited:
            visited.add(node.left)
            queue.append(node.left)
        if node.right and node.right not in visited:
            visited.add(node.right)
            queue.append(node.right)

def run_traversal_visualizations(root: Node):
    """Головна функція для запуску та керування візуалізаціями."""
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 7))

    # Крок 1: Візуалізація DFS
    visualize_dfs(root, ax)

    # Крок 2: Очікування натискання кнопки
    wait_for_button_click(fig)

    # Крок 3: Скидання стану та візуалізація BFS
    reset_node_colors(root)
    visualize_bfs(root, ax)

    # Завершення
    ax.set_title("Обходи завершено!")
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    # Створення дерева
    root            = Node(0)
    root.left       = Node(4)
    root.left.left  = Node(5)
    root.left.right = Node(10)
    root.right      = Node(1)
    root.right.left = Node(3)

    # Запуск процесу візуалізації
    run_traversal_visualizations(root)