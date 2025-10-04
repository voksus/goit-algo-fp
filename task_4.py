# Очистка консолі
print('\033c', end='')

import uuid
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, key, color="skyblue"):
        self.left  : Node = None
        self.right : Node = None
        self.val   = key
        self.color = color # Додатковий аргумент для зберігання кольору вузла
        self.id    = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла

def add_edges(graph: nx.DiGraph, node: Node, pos, x=0, y=0, layer=1):
    if node is not None:
        # Використання id та збереження значення вузла
        graph.add_node(node.id, color=node.color, label=node.val)
    if node.left:
        graph.add_edge(node.id, node.left.id)
        l = x - 1 / 2 ** layer
        pos[node.left.id] = (l, y - 1)
        l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
    if node.right:
        graph.add_edge(node.id, node.right.id)
        r = x + 1 / 2 ** layer
        pos[node.right.id] = (r, y - 1)
        r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    # Використовуйте значення вузла для міток
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()

# Створення дерева
root = Node(0)
root.left = Node(4)
root.left.left = Node(5)
root.left.right = Node(10)
root.right = Node(1)
root.right.left = Node(3)

# Відображення дерева
draw_tree(root)


# ========================================================== #
#       ВІЗУАЛІЗАЦІЯ БІНАРНОЇ КУПИ  (РОЗШИРЕНА ВЕРСІЯ)       #
# Переіряє можливість дерева бути маскимально схожим на купу #
# ========================================================== #

# Кольори
RESET    = '\033[0m'
BOLD     = '\033[1m'
DIM      = '\033[2m'
ITALIC   = '\033[3m'
ULINE    = '\033[4m'
UN_BOLD  = '\033[22m'
UN_ULINE = '\033[24m'
GRAY     = '\033[30m'
RED      = '\033[31m'
GREEN    = '\033[32m'
YELLOW   = '\033[33m'
CYAN     = '\033[36m'
TITLE1   = '\033[1;104m'
TITLE2   = '\033[33;40m'

# Утилітні методи
def bool_decor(value: bool | None) -> str:
    """Декоратор для форматування булевих значень та None з кольорами."""
    match value:
        case True:  return f"{BOLD+GREEN}True{RESET}"
        case False: return f"{BOLD+RED}False{RESET}"
        case None:  return f"{BOLD+YELLOW}None{RESET}"

# --- Існуючі функції для побудови купи з масиву (якщо аналіз провалився) ---
def sift_down_max(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]: largest = left
    if right < n and arr[right] > arr[largest]: largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        sift_down_max(arr, n, largest)

def build_max_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        sift_down_max(arr, n, i)

def list_to_tree(arr, index=0):
    if index < len(arr):
        node = Node(arr[index])
        node.left = list_to_tree(arr, 2 * index + 1)
        node.right = list_to_tree(arr, 2 * index + 2)
        return node
    return None

def tree_to_list_bfs(root_node: Node):
    if not root_node: return []
    values = []
    queue = deque([root_node])
    while queue:
        node = queue.popleft()
        values.append(node.val)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
    return values

# --- Головна функція, що реалізує вашу логіку ---

def analyze_and_draw_heap(root_node: Node):
    """
    Аналізує вхідне бінарне дерево, визначає, чи є воно купою,
    і візуалізує його як є або після перебудови.
    """
    
    # --- Внутрішні допоміжні функції ---
    def _is_complete_tree(root: Node):
        if not root:
            return True
        queue = deque([root])
        found_first_gap = False
        while queue:
            node = queue.popleft()
            if node:
                if found_first_gap:
                    return False
                queue.append(node.left)
                queue.append(node.right)
            else:
                found_first_gap = True
        return True

    def _check_heap_properties(root: Node):
        """
        Перевіряє властивості Min-Heap та Max-Heap за один прохід.
        Повертає:
        - True: якщо це Min-Heap.
        - False: якщо це Max-Heap.
        - None: якщо ні те, ні інше.
        """
        if not root:
            return True # Порожнє дерево вважається купою

        is_min = True
        is_max = True

        def _traverse(node: Node):
            nonlocal is_min, is_max
            if not node:
                return

            if node.left:
                if node.val > node.left.val: is_min = False
                if node.val < node.left.val: is_max = False
                _traverse(node.left)
            
            if node.right:
                if node.val > node.right.val: is_min = False
                if node.val < node.right.val: is_max = False
                _traverse(node.right)
        
        _traverse(root)

        if is_min: return True
        if is_max: return False
        return None
        
    def _rebuild_as_max_heap(node_to_rebuild: Node):
        print("Перебудовуємо дерево у Max-Heap за замовчуванням.")
        values = tree_to_list_bfs(node_to_rebuild)
        print(f"Отримані значення: {values}")
        build_max_heap(values)
        print(f"Значення після перетворення на Max-Heap: {values}")
        return list_to_tree(values)

    # --- Основний блок аналізу та прийняття рішень ---
    print(f"{TITLE1} --- Починаємо глибокий аналіз дерева --- {RESET}\n")
    
    is_structurally_complete = _is_complete_tree(root_node)
    heap_type = _check_heap_properties(root_node)
    
    print(f"Дерево має структуру купи : {bool_decor(is_structurally_complete)}  {DIM+ITALIC}(is_complete, тобто повне дерево){RESET}")
    print(f"Тип властивостей для купи : {bool_decor(heap_type)}  "
          f"{ITALIC+DIM}(значення {bool_decor(True)+ITALIC+DIM} => {ULINE}Min{UN_ULINE} , "
          f"{bool_decor(False)+ITALIC+DIM} => {ULINE}Max{UN_ULINE} , "
          f"{bool_decor(None)+ITALIC+DIM} => {ULINE}Neither{UN_ULINE}){RESET}")
    
    if is_structurally_complete:
        match heap_type:
            case True:
                print(f"\n{TITLE2} ВИСНОВОК: Дерево вже є коректною Min-Heap. Візуалізуємо як є.{RESET}")
            case False:
                print(f"\n{TITLE2} ВИСНОВОК: Дерево вже є коректною Max-Heap. Візуалізуємо як є.{RESET}")
            case None: # або case _:
                print(f"\n{TITLE2} ВИСНОВОК: Структура коректна, але значення не впорядковані як купа.{RESET}")
                root_node = _rebuild_as_max_heap(root_node)
    else:
        print(f"\n{TITLE2} ВИСНОВОК: Структура дерева не є повною. Потрібна перебудова. {RESET}")
        root_node = _rebuild_as_max_heap(root_node)

    # Візуалізація фінального стану дерева (купи)
    draw_tree(root_node)

# Виклик нової "розумної" функції
analyze_and_draw_heap(root)