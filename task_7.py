# Очистка консолі
print('\033c', end='')

import numpy as np
import matplotlib.pyplot as plt

def simulate_dice_rolls_monte_carlo(num_rolls: int = 1000):
    """
    Симулює кидання двох гральних кубиків методом Монте-Карло,
    візуалізує результати та виводить таблицю ймовірностей.
    """
    # Крок 1: Симуляція кидків для двох кубиків
    # Генеруємо num_rolls випадкових цілих чисел від 1 до 6 (включно) для кожного кубика
    die1_rolls = np.random.randint(1, 7, size=num_rolls)
    die2_rolls = np.random.randint(1, 7, size=num_rolls)
    
    # Крок 2: Розрахунок сум для кожного кидка
    # Просто додаємо відповідні результати кидків
    sums = die1_rolls + die2_rolls
    
    # Крок 3: Підрахунок частоти кожної суми
    # np.unique повертає унікальні значення та їх кількість
    possible_sums, counts = np.unique(sums, return_counts=True)
    
    # Створюємо словник для зручності: {сума: кількість}
    frequencies = dict(zip(possible_sums, counts))
    
    # Крок 4: Візуалізація результатів (графік)
    # Визначаємо повний діапазон можливих сум (від 2 до 12)
    x_values = range(2, 13)
    # Для кожної можливої суми беремо її частоту (або 0, якщо вона не випала)
    y_values = [frequencies.get(s, 0) for s in x_values]
    y_max = max(y_values)
    
    plt.figure(figsize=(10, 6))
    bars: plt.BarContainer = plt.bar(x_values, y_values, color='skyblue', edgecolor='black')
    for bar in bars:
        yval = bar.get_height()  # Висота стовпчика (значення Y)
        xval = bar.get_x() + bar.get_width() / 2  # Центр стовпчика (значення X)
        
        # Використовуємо plt.text для додавання тексту
        plt.text(xval, yval,
            yval,
            ha='center', va='bottom',
            color='darkred', fontsize=12, fontweight='bold'
        )
        plt.text(xval, yval - y_max * 0.037,
            f'{frequencies[xval] / num_rolls:.2%}',
            ha='center', va='bottom',
            color='blue', fontsize=8,
            fontstyle='italic', fontweight='bold', alpha=0.5
        )
    plt.title(f'Частота сум при киданні двох кубиків ({num_rolls:,} спроб)'.replace(',', '\''), fontdict={'weight': 'bold', 'size': 14})
    plt.xlabel('Сума очок на кубиках', fontdict={'weight': 'bold', 'size': 12})
    plt.ylabel('Кількість випадків', fontdict={'weight': 'bold', 'size': 12})
    plt.xticks(x_values) # Переконуємось, що всі значення по осі Х відображені
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.show()
    
    # Крок 5: Розрахунок та виведення таблиці ймовірностей
    print("Таблиця ймовірностей за результатами симуляції:\n")
    print("| Сума | Імовірність | Всього випадань |")
    print("|------|-------------|-----------------|")
    
    # Сортуємо суми для впорядкованого виводу
    sorted_sums = sorted(frequencies.keys())
    
    for s in sorted_sums:
        count = frequencies[s]
        probability = count / num_rolls
        print(f"|  {s:>2}  | {probability:^11.2%} | {count:^15,} |".replace(',', '\''))
    print()


if __name__ == '__main__':
    NUMBER_OF_SIMULATIONS = 80_000
    simulate_dice_rolls_monte_carlo(NUMBER_OF_SIMULATIONS)