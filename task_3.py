# Очистка консолі
print('\033c', end='')

import networkx as nx
import matplotlib.pyplot as plt
import heapq

# --- 1. Набір даних та Мапування ---
# Глобальний словник для мапування літер (ключ) на повну назву завдання (значення)
TASK_MAP = {
    "A": "A - Аналіз вимог",        "B": "B - Прототип",           "C": "C - Розробка API",
    "D": "D - Тестування",          "E": "E - Налаштування CI/CD", "F": "F - Верстка UI",
    "G": "G - Інтеграція платежів", "H": "H - Безпека",            "I": "I - Міграція даних",
    "J": "J - Документація",        "K": "K - A/B Тестування",     "L": "L - MVP Реліз",
    "M": "M - Звітність",           "N": "N - Рефакторинг",        "O": "O - Розширення API",
    "P": "P - Навчання команди",    "Q": "Q - Моніторинг",         "R": "R - Дизайн БД",
    "S": "S - Огляд коду",          "T": "T - Фінальний реліз"
}

# --- ХАРДКОДОВАНІ ПОЗИЦІЇ ДЛЯ ІЄРАРХІЧНОЇ ВІЗУАЛІЗАЦІЇ (ЗЛІВА НАПРАВО) ---
# Координати: { Вузол: (X-координата (шар), Y-координата (вертикальне зміщення)) }
INITIAL_POS = {
    # СТАРТ (Layer 0)
    "A": (0, 0),

    # РІВЕНЬ 1 (Layer 1) - Паралельні гілки
    "R": (1, 3),   # Прототип (UI branch)
    "B": (1, -3),  # Дизайн БД (Core/API branch)

    # РІВЕНЬ 2 (Layer 2)
    "F": (2, 4),   # Верстка UI
    "C": (2, 0),   # Розробка API
    "I": (2, -4),  # Міграція даних

    # РІВЕНЬ 3 (Layer 3)
    "G": (3, 1),   # Інтеграція платежів (з F і C)
    "D": (3, -2),  # Тестування
    "O": (3, 3),   # Розширення API

    # РІВЕНЬ 4 (Layer 4)
    "K": (4, 2),    # A/B Тестування
    "S": (4, 4),    # Огляд коду
    "H": (4, 0),    # Безпека
    "E": (4, -1.5), # Налаштування CI/CD
    "J": (4, -4),   # Документація

    # РІВЕНЬ 5 (Layer 5)
    "N": (5, 3),    # Рефакторинг (від S)
    "L": (5, -1),   # MVP Реліз (ТОЧКА КОНВЕРГЕНЦІЇ)

    # РІВЕНЬ 6 (Layer 6) - Пост-MVP
    "M": (6, 0),    # Звітність
    "P": (6, -1.5), # Навчання команди
    "Q": (6, 2),    # Моніторинг (від N)

    # РІВЕНЬ 7 (Layer 7) - Фінал
    "T": (7, 0)     # Фінальний реліз
}

def get_full_name(short_name):
    """Отримує повну назву завдання за його літерним позначенням."""
    return TASK_MAP.get(short_name, short_name)

def create_task_graph():
    """Створює спрямований ациклічний граф (DAG) для моделювання залежностей завдань."""
    G = nx.DiGraph()

    # Вершини - тепер просто літери (ключі з TASK_MAP)
    tasks = list(TASK_MAP.keys())
    G.add_nodes_from(tasks)

    # Залежності (Ребра з Вагами) - тепер використовуємо тільки літерні позначення
    # Формат: (Попередник, Наступне Завдання, Вага (час))
    dependencies = [
        ("A", "B", 8),  ("A", "R", 4),
        ("R", "F", 12), ("B", "C", 15), ("B", "I", 10),
        ("C", "D", 5),  ("C", "O", 12), ("C", "G", 9),
        ("F", "G", 6),  ("F", "S", 3),
        ("D", "E", 7),  ("D", "H", 5),
        ("G", "H", 4),  ("G", "K", 8),
        ("I", "J", 2),  ("O", "S", 4),  ("S", "N", 6), ("N", "Q", 5),
        ("E", "L", 3),  ("H", "L", 2),  ("J", "L", 1), ("K", "L", 4),
        ("L", "M", 5),  ("L", "P", 4),
        ("M", "T", 2),  ("Q", "T", 1),  ("P", "T", 1),
    ]

    for u, v, weight in dependencies:
        G.add_edge(u, v, weight=weight)

    return G

# --- 2. Функція Візуалізації Графа (для ітеративного режиму) ---
def visualize_graph(G, pos=None, start_node=None, title="Граф Залежностей Проєкту",
                    node_colors=None, edge_colors=None, node_labels_extra=None,
                    path_text=None):
    """
    Візуалізує граф за допомогою matplotlib і networkx.
    Використовує plt.clf() та plt.pause() для ітеративної візуалізації.
    """

    # Очистка фігури для нового кадру
    plt.clf()

    # Встановлення заголовка
    plt.title(title, fontsize=20, color='#333333')

    # Визначення позицій вершин для стабільної візуалізації
    if pos is None:
        # Якщо позиція не передана (хоча вона повинна бути хардкодована), 
        # повертаємося до spring_layout як резервного варіанту.
        pos = nx.spring_layout(G, k=0.8, iterations=50) 

    # Налаштування кольорів та розмірів для всіх вершин
    if node_colors is None:
        node_colors = ['#ADD8E6' if node == start_node else '#B0C4DE' for node in G.nodes()]

    node_size = 2000

    # Мітки - тепер просто літери
    labels = {node: node for node in G.nodes()}

    # Малювання вершин
    nx.draw_networkx_nodes(G, pos, 
                           node_color=node_colors, 
                           node_size=node_size, 
                           edgecolors='#333333', 
                           linewidths=1.5,
                           alpha=0.9)

    # Малювання ребер
    nx.draw_networkx_edges(G, pos, 
                           edge_color=edge_colors if edge_colors is not None else '#AAAAAA', 
                           width=1.5, 
                           arrowsize=20, 
                           alpha=0.6,
                           min_target_margin=25,
                           min_source_margin=25)

    # Малювання міток вершин (A, B, C...)
    nx.draw_networkx_labels(G, pos, 
                            labels=labels, 
                            font_size=14, 
                            font_color='black', 
                            font_weight='bold')

    # Малювання ваг ребер
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, 
                                 edge_labels=edge_labels, 
                                 font_color='#777777', 
                                 font_size=10)

    # Малювання додаткових міток (відстані)
    if node_labels_extra is not None:
         # Зміщуємо мітки трохи вниз, щоб не перекривати основні мітки (літери)
         label_pos_extra = {k: [v[0], v[1] - 0.25] for k, v in pos.items()}
         nx.draw_networkx_labels(G, label_pos_extra, 
                                labels=node_labels_extra, 
                                font_size=9, 
                                font_color='darkred',
                                font_weight='bold')

    # Додавання Легенди та Фінального Маршруту
    legend_text = "ЛЕГЕНДА ЗАВДАНЬ:"
    for short, full in TASK_MAP.items():
        # Отримуємо опис завдання, відкидаючи літеру
        description = full.split(' - ')[1] 
        legend_text += f"\n{short}: {description}"

    if path_text:
        # Додавання знайденого найкоротшого маршруту
        legend_text += f"\n\nНАЙКОРОТШИЙ ШЛЯХ:\n{path_text}"

    # Використовуємо plt.text для виведення легенди в лівому верхньому куті полотна
    plt.text(0.02, 0.98, legend_text, 
             transform=plt.gcf().transFigure,
             fontsize=10, 
             verticalalignment='top', 
             bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.9, edgecolor='gray'))

    # Приховати осі
    plt.axis('off')

    # Пауза для відображення змін
    plt.pause(0.25)

# Функція для відновлення шляху на основі попередників
def reconstruct_path(predecessors, start, end):
    """Відновлює найкоротший шлях від 'end' до 'start' за словником попередників."""
    path = []
    current = end
    while current != start:
        if current not in predecessors:
            return [] # Шлях не знайдено
        path.append(current)
        current = predecessors[current]
    path.append(start)
    path.reverse()
    return path


# --- 3. Власна Реалізація Алгоритму Дейкстри як Генератора ---
def dijkstra_step_by_step_generator(G, source):
    """
    Реалізація алгоритму Дейкстри з використанням heapq (Min Heap)
    як генератора для покрокової візуалізації.
    """
    # Ініціалізація: відстані до всіх вузлів нескінченні, крім початкового
    distances = {node: float('inf') for node in G.nodes()}
    distances[source] = 0

    # Словник для зберігання попередників для відновлення шляху
    predecessors = {node: None for node in G.nodes()}

    # Черга з пріоритетами (Min Heap): (відстань, вузол)
    priority_queue = [(0, source)]

    # Множина для відвіданих/зафіксованих вузлів
    visited_nodes = set()

    # Початковий стан (Крок 1)
    yield {
        'distances'      : distances.copy(),
        'visited'        : set(),
        'current_node'   : None,
        'processed_edges': [],
        'predecessors'   : predecessors.copy()
    }

    while priority_queue:
        # 1. Витягуємо вузол з найменшою поточною відстанню (жадібний вибір)
        current_distance, current_node = heapq.heappop(priority_queue)

        # Якщо вузол вже відвіданий/зафіксований, пропускаємо його (стара відстань)
        if current_node in visited_nodes:
            continue

        # Позначаємо вузол як відвіданий/зафіксований
        visited_nodes.add(current_node)

        # Стан для поточної ітерації
        state = {
            'distances'      : distances.copy(),
            'visited'        : visited_nodes.copy(),
            'current_node'   : current_node,
            'processed_edges': [],
            'predecessors'   : predecessors.copy() # Передаємо поточних попередників
        }

        # 2. Обробка сусідів (Релаксація)
        for neighbor, data in G[current_node].items():
            weight = data.get('weight', 1) # Беремо вагу, або 1 за замовчуванням
            new_distance = current_distance + weight

            # Якщо знайдено коротший шлях до сусіда, оновлюємо його відстань
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                # *** Збереження попередника (Ключовий крок для відновлення шляху) ***
                predecessors[neighbor] = current_node
                # ********************************************************************

                # Додаємо або оновлюємо сусіда в черзі з новою, меншою відстанню
                heapq.heappush(priority_queue, (new_distance, neighbor))

                # Додаємо ребро, яке було релаксовано, для підсвічування
                state['processed_edges'].append((current_node, neighbor))

        # 3. Повертаємо поточний стан для візуалізації
        yield state

    # Фінальний стан (Повертаємо фінальні відстані та попередники)
    yield {
        'distances'      : distances.copy(),
        'visited'        : visited_nodes.copy(),
        'current_node'   : None,
        'processed_edges': [],
        'predecessors'   : predecessors.copy() 
    }

# --- 4. Основна Логіка (Виклик) ---
if __name__ == "__main__":

    # Створюємо граф
    ProjectGraph = create_task_graph()

    # Визначаємо початкову вершину для алгоритму Дейкстри
    START_TASK = "A"

    # Визначаємо кінцеву вершину 
    END_TASK = "L"

    # Вмикаємо інтерактивний режим візуалізації 
    plt.ion()
    # Створюємо фігуру один раз перед циклом
    fig = plt.figure(figsize=(20, 12)) 

    step_num = 0
    final_state = None # Зберігаємо фінальний стан

    # Запуск генератора власного алгоритму Дейкстри
    dijkstra_steps = dijkstra_step_by_step_generator(ProjectGraph, START_TASK)

    for state in dijkstra_steps:
        step_num += 1
        final_state = state # Зберігаємо кожен стан, щоб мати фінальний після циклу

        # 1. Визначення кольорів вершин на основі стану
        node_colors = []
        node_labels_extra = {} # Мітки для відстаней (distance)

        for node in ProjectGraph.nodes():
            distance = state['distances'][node]
            # Форматуємо мітку відстані (ціле число або 'inf')
            node_labels_extra[node] = f"{distance:.0f}" if distance != float('inf') else 'inf'

            if node in state['visited'] and node != state['current_node']:
                # Закриті/Фіналізовані вершини (Світло-сірі)
                node_colors.append('#BBBBBB') # LightGray
            elif node == state['current_node']:
                # Активно оброблювана вершина (Червоний/Помаранчевий)
                node_colors.append('#FFA07A') # LightSalmon
            elif distance != float('inf'):
                # Відвідані, але ще не фіналізовані (в черзі) (Жовтий)
                node_colors.append('#FFFFE0') # LightYellow
            else:
                # Не відвідані (Синій)
                node_colors.append('#ADD8E6') # LightBlue

        # 2. Визначення кольорів ребер на основі стану (підсвічуємо релаксовані)
        edge_colors_map = {edge: '#AAAAAA' for edge in ProjectGraph.edges()}
        edges_to_highlight = state['processed_edges']

        for edge in edges_to_highlight:
            # Ребра, які були оновлені/релаксовані на поточному кроці
            edge_colors_map[edge] = 'red'

        # Створюємо список кольорів у порядку ребер графа
        edge_colors = [edge_colors_map[edge] for edge in ProjectGraph.edges()]

        # 3. Візуалізація
        if state['current_node']:
            current_node_short = state['current_node']
            current_distance_val = state['distances'][state['current_node']]
            current_title = f"Крок {step_num}: Обробка вузла {current_node_short} (відстань: {current_distance_val})"
        elif step_num == 1:
            current_title = "Крок 1: Ініціалізація (A=0, решта=inf)"
        else:
            # На цьому кроці алгоритм завершено, але візуалізація фінального шляху буде нижче
            current_title = f"Крок {step_num}: Алгоритм завершено. Фінальні відстані знайдено."

        visualize_graph(ProjectGraph, 
                        pos=INITIAL_POS, # Використовуємо хардкодовані позиції
                        start_node=START_TASK, 
                        title=current_title,
                        node_colors=node_colors,
                        edge_colors=edge_colors,
                        node_labels_extra=node_labels_extra)

    # --- 5. ФІНАЛЬНА ВІЗУАЛІЗАЦІЯ НАЙКОРОТШОГО МАРШРУТУ ---
    if final_state and END_TASK in final_state['predecessors']:

        # Відновлюємо найкоротший шлях
        shortest_path = reconstruct_path(final_state['predecessors'], START_TASK, END_TASK)

        # Визначаємо ребра, які належать цьому шляху
        path_edges = []
        for i in range(len(shortest_path) - 1):
            path_edges.append((shortest_path[i], shortest_path[i+1]))

        # Готуємо текстовий вивід шляху
        path_text = " -> ".join(shortest_path)
        final_distance = final_state['distances'][END_TASK]

        final_title = (f"ФІНАЛ: Найкоротший шлях до {END_TASK} ({TASK_MAP[END_TASK]}) знайдено! "
                       f"Час: {final_distance:.0f}")

        # Перемальовуємо кольори для фінального кадру
        final_node_colors = []
        final_edge_colors_map = {edge: '#AAAAAA' for edge in ProjectGraph.edges()}

        # Підсвічуємо вершини шляху (LightGreen)
        for node in ProjectGraph.nodes():
            if node in shortest_path:
                final_node_colors.append('#90EE90') # LightGreen
            else:
                final_node_colors.append('#BBBBBB') # LightGray (Закриті)

        # Підсвічуємо ребра шляху (DarkGreen)
        for edge in path_edges:
            final_edge_colors_map[edge] = '#226622'

        final_edge_colors = [final_edge_colors_map[edge] for edge in ProjectGraph.edges()]

        # Фінальна візуалізація з підсвічуванням шляху та текстовою інформацією
        visualize_graph(ProjectGraph, 
                        pos=INITIAL_POS, 
                        start_node=START_TASK, 
                        title=final_title,
                        node_colors=final_node_colors,
                        edge_colors=final_edge_colors,
                        node_labels_extra=node_labels_extra, # Зберігаємо фінальні відстані
                        path_text=path_text)

    # В кінці вимикаємо інтерактивний режим і залишаємо фінальне вікно
    plt.ioff()
    plt.show()