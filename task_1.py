# Очистка консолі
print('\033c', end='')

# Головні налаштування
# Кольори
RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'
GRAY   = '\033[30m'
RED    = '\033[31m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
CYAN   = '\033[36m'
# Шаблони
TITLE = '\033[1;104m'

# Утилітні методи
def print_title(title):
    """
    Виводить заголовок з оформленням.

    Args:
        title (str): Текст заголовка.
    """
    print(f"{TITLE} {title} {RESET}")

def print_sub1(subtitle):
    """
    Виводить підзаголовок першого типу з оформленням.

    Args:
        title (str): Текст підзаголовка.
    """
    print(f"  {BOLD+YELLOW}{subtitle}{RESET}")

def print_sub2(subtitle):
    """
    Виводить підзаголовок першого типу з оформленням.

    Args:
        title (str): Текст підзаголовка.
    """
    print(f"  {BOLD+RED}{subtitle}{RESET}")


class Node:
    """
    Клас для представлення вузла однозв'язного списку.
    Кожен вузол містить дані та посилання на наступний вузол.
    """
    def __init__(self, data=None):
        """
        Ініціалізація вузла.

        Args:
            data: Дані, які зберігатиме вузол.
        """
        self.data = data
        self.next = None


class LinkedList:
    """
    Клас для реалізації однозв'язного списку.
    Містить посилання на головний (перший) вузол списку.
    """
    def __init__(self):
        """
        Ініціалізація порожнього списку.
        """
        self.head = None

    def __str__(self) -> str:
        """
        Створює рядок зі вмістом списку.
        """
        current_node = self.head
        elements = []
        while current_node:
            elements.append(str(current_node.data))
            current_node = current_node.next
        return '    ' + f' {GRAY}->{RESET} '.join(BOLD + GREEN + el + RESET for el in elements)

    def append(self, data):
        """
        Додає новий вузол з даними в кінець списку.

        Args:
            data: Дані для нового вузла.
        """
        new_node = Node(data)
        if self.head is None:
            # Якщо список порожній, новий вузол стає головним
            self.head = new_node
            return
        # Інакше, йдемо до кінця списку
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        # Додаємо новий вузол в кінець
        last_node.next = new_node

    def reverse(self):
        """
        Реверсує однозв'язний список, змінюючи посилання між вузлами.
        """
        prev_node = None
        current_node = self.head
        while current_node is not None:
            # Зберігаємо посилання на наступний вузол, щоб не втратити його
            next_node = current_node.next
            # Змінюємо посилання поточного вузла, щоб він вказував на попередній
            current_node.next = prev_node
            # Рухаємося далі по списку: попередній вузол стає поточним
            prev_node = current_node
            # А поточний - наступним, що збережений раніше
            current_node = next_node
        # В кінці prev_node буде вказувати на новий головний вузол
        self.head = prev_node

    def insertion_sort(self):
        """
        Сортує однозв'язний список, використовуючи алгоритм сортування вставками.
        """
        # Перевірка, чи список порожній або має лише один елемент
        if self.head is None or self.head.next is None:
            return

        sorted_head = None  # Голова нового, відсортованого списку
        current = self.head

        while current:
            next_node_to_process = current.next  # Зберігаємо наступний вузол для обробки

            # Вставляємо 'current' у відсортований список 'sorted_head'
            if sorted_head is None or sorted_head.data >= current.data:
                # Якщо відсортований список порожній або новий елемент менший за голову
                current.next = sorted_head
                sorted_head = current
            else:
                # Шукаємо місце для вставки у відсортованій частині
                search_node = sorted_head
                while search_node.next and search_node.next.data < current.data:
                    search_node = search_node.next
                # Вставляємо вузол
                current.next = search_node.next
                search_node.next = current

            current = next_node_to_process # Переходимо до наступного вузла з оригінального списку

        # Оновлюємо голову нашого списку
        self.head = sorted_head


def merge_sorted_lists(list1: LinkedList, list2: LinkedList) -> LinkedList:
    """
    Об'єднує два відсортовані однозв'язні списки в один новий відсортований список.

    Args:
        list1 (LinkedList): Перший відсортований список.
        list2 (LinkedList): Другий відсортований список.

    Returns:
        LinkedList: Новий об'єднаний та відсортований список.
    """
    # Створюємо "фіктивний" вузол, щоб спростити код
    dummy_node = Node()
    # 'tail' буде вказувати на останній вузол у новому списку
    tail = dummy_node

    p1 = list1.head
    p2 = list2.head

    # Поки обидва списки не закінчились
    while p1 and p2:
        if p1.data <= p2.data:
            tail.next = p1
            p1 = p1.next
        else:
            tail.next = p2
            p2 = p2.next
        # Переміщуємо 'tail' на щойно доданий вузол
        tail = tail.next

    # Якщо в одному зі списків залишились елементи, додаємо їх в кінець
    if p1:
        tail.next = p1
    elif p2:
        tail.next = p2

    # Створюємо новий об'єкт списку
    merged_list = LinkedList()
    # Голова нового списку - це наступний вузол після фіктивного
    merged_list.head = dummy_node.next
    return merged_list


def main():
    """
    Головна функція для демонстрації роботи зі списком.
    """
    # --- 1. Демонстрація реверсування списку ---
    print_title("1. Реверсування списку:")
    llist_rev = LinkedList()
    llist_rev.append(1)
    llist_rev.append(2)
    llist_rev.append(3)
    llist_rev.append(4)

    print_sub1("Оригінальний список:")
    print(llist_rev)

    # -----------------------
    # 1. Реверсуввання списку
    # -----------------------
    llist_rev.reverse()
    # -----------------------
    print_sub2("Реверсований список:")
    print(llist_rev)
    print("-" * 20 + '\n')

    # --- 2. Демонстрація сортування списку ---
    print_title("2. Сортування списку (вставками):")
    llist_sort = LinkedList()
    llist_sort.append(40)
    llist_sort.append(20)
    llist_sort.append(60)
    llist_sort.append(10)
    llist_sort.append(50)
    llist_sort.append(30)

    print_sub1("Список до сортування:")
    print(llist_sort)

    # ------------------------------
    # 2. Сортування списку вставками
    # ------------------------------
    llist_sort.insertion_sort()
    # ------------------------------
    print_sub2("Список після сортування:")
    print(llist_sort)
    print("-" * 20 + '\n')

    # --- 3. Демонстрація об'єднання двох відсортованих списків ---
    print_title("3. Об'єднання двох відсортованих списків")
    llist1 = LinkedList()
    llist1.append(5)
    llist1.append(10)
    llist1.append(15)

    llist2 = LinkedList()
    llist2.append(2)
    llist2.append(3)
    llist2.append(20)

    print_sub1("1-й відсортований список:")
    print(llist1)
    print_sub1("2-й відсортований список:")
    print(llist2)

    # ----------------------------------------
    # 3. Об'єднання двох відсортованих списків
    # ----------------------------------------
    merged_list = merge_sorted_lists(llist1, llist2)
    # ----------------------------------------
    print_sub2("Об'єднаний відсортований список:")
    print(merged_list)
    print("-" * 20)


# Точка входу в програму
if __name__ == "__main__":
    main()