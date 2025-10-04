# Очистка консолі
print('\033c', end='')

# Кольори
RESET   = '\033[0m'
BOLD    = '\033[1m'
DIM     = '\033[2m'
UNDECOR = '\033[22m'
RED     = '\033[31m'
L_BLUE  = '\033[38;2;220;220;255m'
L_GREEN = '\033[38;2;220;255;220m'
TITLE0  = '\033[1;104m'
TITLE1  = '\033[48;2;184;168;100;38;2;8;0;8m'
TITLE2A = '\033[48;2;8;32;56;38;2;220;220;220m'
TITLE2B = '\033[48;2;8;56;32;38;2;220;220;220m'

# Задані дані про їжу
items: dict[str, dict[str, int]] = {
    "pizza"     : {"cost" : 50, "calories" : 300},
    "hamburger" : {"cost" : 40, "calories" : 250},
    "hot-dog"   : {"cost" : 30, "calories" : 200},
    "pepsi"     : {"cost" : 10, "calories" : 100},
    "cola"      : {"cost" : 15, "calories" : 220},
    "potato"    : {"cost" : 25, "calories" : 350}
}

# Утилітні методи
def values_list_decor(values: dict[str, int]) -> str:
    """Декоратор для форматування списку значень з кольорами."""
    return ', '.join(f'{UNDECOR}"{k}"{DIM}: {UNDECOR}{v}шт.{DIM}' for k, v in values.items())

def view_result_with_budget(budget: int):
    """Виводить результати роботи обох алгоритмів для заданого бюджету."""
    print(f'{TITLE1} Заданий бюджет: {BOLD}{budget}{UNDECOR}₴ ░▒▓{RESET}')

    def _view_calculated_result(color: str, result: tuple[int, int, dict[str, int]]):
        """Виводить результати обчислень обох алгоритмів."""
        if result[0]:
            print(f'{color+DIM} ┗╾╴Витрачено: {UNDECOR}{result[0]}{DIM}₴{RESET}', end='  ')
            print(f'{color+DIM}Калорійність: {UNDECOR}{result[1]}{RESET}', end='  ')
            print(f'{color+DIM}Обрані страви: {UNDECOR}{values_list_decor(result[2])}{RESET}')
        else:
            print(f'{RED}Нічого не обрано.{RESET}')

    # Виклик жадібного алгоритму
    greedy_result = greedy_algorithm(items, budget)
    print(f'{TITLE2A} Жадібний алгоритм: {RESET}')
    _view_calculated_result(L_BLUE, greedy_result)

    # Виклик алгоритму динамічного програмування
    dp_result = dynamic_programming(items, budget)
    print(f'{TITLE2B} Алгоритм динамічного програмування: {RESET}')
    _view_calculated_result(L_GREEN, dp_result)
    print()

def greedy_algorithm(items: dict[str, dict[str, int]], budget: int) -> tuple[int, int, dict[str, int]]:
    """
    Реалізує жадібний алгоритм для вибору їжі, дозволяючи брати
    декілька одиниць одного товару.

    На кожному кроці вибирається страва з найкращим співвідношенням 
    калорій до вартості, поки не буде перевищено бюджет.
    """
    # Сортуємо страви за спаданням співвідношення калорій до вартості
    sorted_items = sorted(items.items(), 
                          key=lambda x: x[1]['calories'] / x[1]['cost'], 
                          reverse=True)

    total_cost = 0
    total_calories = 0
    chosen_items: dict[str, int] = {}

    # Проходимо по відсортованих стравах
    for item_name, item_data in sorted_items:
        cost = item_data['cost']
        # Додаємо поточну страву стільки разів, скільки дозволяє бюджет
        while total_cost + cost <= budget:
            # Додаємо страву до результату, збільшуючи лічильник
            chosen_items[item_name] = chosen_items.get(item_name, 0) + 1
            total_cost += cost
            total_calories += item_data['calories']

    return total_cost, total_calories, chosen_items

def dynamic_programming(items: dict[str, dict[str, int]], budget: int) -> tuple[int, int, dict[str, int]]:
    """
    Реалізує алгоритм динамічного програмування для задачі
    про необмежений рюкзак (Unbounded Knapsack Problem).

    Гарантує знаходження оптимального набору страв, що максимізує
    сумарну калорійність в межах заданого бюджету.
    """
    # dp[i] зберігатиме максимальну калорійність для бюджету i
    dp = [0] * (budget + 1)
    # last_item[i] зберігатиме назву останньої страви, доданої для досягнення
    # оптимального результату для бюджету i
    last_item = [''] * (budget + 1)

    # Ітеруємо по кожному можливому значенню бюджету від 1 до заданого
    for w in range(1, budget + 1):
        # Для кожного бюджету перевіряємо всі можливі страви
        for item_name, item_data in items.items():
            cost = item_data['cost']
            calories = item_data['calories']
            
            # Якщо страва вміщується в поточний бюджет w
            # і якщо її додавання покращує результат для цього бюджету
            if cost <= w and dp[w - cost] + calories > dp[w]:
                dp[w] = dp[w - cost] + calories
                last_item[w] = item_name

    # Відновлюємо набір обраних страв, рухаючись назад від кінцевого бюджету
    total_cost = 0
    total_calories = dp[budget]
    chosen_items: dict[str, int] = {}
    current_budget = budget

    while current_budget > 0 and last_item[current_budget]:
        item_name = last_item[current_budget]
        item_cost = items[item_name]['cost']
        
        # Додаємо знайдену страву до результату
        chosen_items[item_name] = chosen_items.get(item_name, 0) + 1
        total_cost += item_cost
        current_budget -= item_cost
        
    return total_cost, total_calories, chosen_items

# Приклад використання
if __name__ == "__main__":
    print(f'{TITLE0} Порівняння жадібного алгоритму та алгоритму динамічного програмування для задачі вибору їжі з обмеженим бюджетом. {RESET}\n')
    # Перевірка роботи алгоритмів з різними бюджетами
    for budget in [35, 45, 95, 100, 125]:
        view_result_with_budget(budget)