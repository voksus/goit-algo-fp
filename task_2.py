# Очистка консолі
print('\033c', end='')

import math
import sys
import matplotlib.pyplot as plt
import math

# Інтерактивний метод (бонусний).
# Використовує PyGame для візуалізації.
class PythagorasTree:
    """
    Клас для створення та візуалізації фрактала "Дерево Піфагора"
    за допомогою pygame з інтерактивними елементами керування.
    """

    def __init__(self, width=1200, height=600):
        """
        Ініціалізація програми, налаштувань pygame та початкових параметрів дерева.
        """
        pygame.init()

        # Налаштування екрану
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Інтерактивне Дерево Піфагора")

        # Кольори
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_PALE_GREEN = (152, 251, 152)
        self.COLOR_GRAY = (100, 100, 100)
        self.COLOR_WHITE = (220, 220, 220)
        self.COLOR_GREEN = (80, 255, 80)
        # Позиція елементу інтерфейсу "Рівень рекурсії"
        self.POS_RX1 = 50  # Позиція X для рядка "Рівень рекурсії"
        self.POS_RX2 = 215 # Позиція X для кнопок лічільника рівня рекурсії
        self.POS_RX3 = 255 # Позиція X для значення рівня рекурсії
        self.POS_RY1 = self.height - 50 # Позиція Y для значення рівня рекурсії
        # Позиція елементу інтерфейсу "Нахил"
        self.POS_AX1 = self.width  - 300 # Позиція X для рядка "Нахил"
        self.POS_AX2 = self.POS_AX1 + 70 # Позиція X для рядка "Нахил"
        self.POS_AY1 = self.height  - 70 # Позиція Y для налаштування нахилу

        # Шрифти для інтерфейсу
        self.font = pygame.font.Font(None, 28)

        # Параметри фрактала за замовчуванням
        self.recursion_level = 8
        self.tilt_angle = 0  # Нахил в градусах, від -30 до +30

        # Початкові параметри стовбура дерева
        self.start_pos = (self.width // 2, self.height - 50)
        self.base_length = 150
        self.base_angle = -90  # Напрямок дереа вгору
        self.base_thickness = 7

        # Змінні для стану інтерфейсу
        self.is_drawing = False
        self.is_dragging_slider = False
        self.needs_redraw = True  # Прапорець для перемальовування

        # Геометрія елементів керування
        self._setup_ui_rects()

    def _setup_ui_rects(self):
        """Ініціалізує pygame.Rect об'єкти для елементів інтерфейсу."""
        # Лічильник рівня рекурсії
        self.level_label_pos = (self.POS_RX1, self.POS_RY1)
        self.level_value_pos = (self.POS_RX3, self.POS_RY1)
        self.level_up_button_rect = pygame.Rect(self.POS_RX2, self.POS_RY1 - 18, 25, 25)
        self.level_down_button_rect = pygame.Rect(self.POS_RX2, self.POS_RY1 + 10, 25, 25)

        # Повзунок нахилу
        self.tilt_label_pos1 = (self.POS_AX1, self.POS_AY1)
        self.tilt_label_pos2 = (self.POS_AX2, self.POS_AY1)
        self.slider_track_rect = pygame.Rect(self.POS_AX1 - 100, self.POS_AY1 + 30, 300, 10)
        # Ручка повзунка буде розраховуватися динамічно

    def run(self):
        """Головний цикл програми."""
        clock = pygame.time.Clock()
        running = True

        while running:
            # Обробка подій (кліки, рух миші, закриття вікна)
            running = self.handle_events()

            # Оновлення та малювання, якщо є зміни
            if self.needs_redraw:
                self.draw()
                self.needs_redraw = False

            clock.tick(60)  # Обмеження FPS

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Обробляє всі події від користувача."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Сигнал для завершення головного циклу

            # Не обробляти нові кліки, поки йде малювання
            if self.is_drawing:
                continue

            # --- Обробка натискання кнопки миші ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Ліва кнопка миші
                    mouse_pos = pygame.mouse.get_pos()
                    # Перевірка кліку по кнопках лічильника
                    if self.level_up_button_rect.collidepoint(mouse_pos):
                        self.recursion_level = min(15, self.recursion_level + 1)
                        self.needs_redraw = True
                    elif self.level_down_button_rect.collidepoint(mouse_pos):
                        self.recursion_level = max(1, self.recursion_level - 1)
                        self.needs_redraw = True
                    # Перевірка кліку по повзунку
                    elif self.slider_track_rect.collidepoint(mouse_pos):
                        self.is_dragging_slider = True
                        self._update_slider(mouse_pos)

            # --- Обробка відпускання кнопки миші ---
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_dragging_slider = False

            # --- Обробка руху миші ---
            elif event.type == pygame.MOUSEMOTION:
                if self.is_dragging_slider:
                    self._update_slider(event.pos)

        return True

    def _update_slider(self, mouse_pos):
        """Оновлює значення кута нахилу на основі позиції миші."""
        # Обмежуємо позицію миші межами треку повзунка
        relative_x = mouse_pos[0] - self.slider_track_rect.x
        clamped_x = max(0, min(self.slider_track_rect.width, relative_x))
        
        # Переводимо позицію в діапазон [-30, 30]
        percentage = clamped_x / self.slider_track_rect.width
        angle_range = 60  # від -30 до +30
        new_angle = (percentage * angle_range) - 30
        
        # Дискретизація з кроком 0.1 градуса
        discretized_angle = round(new_angle, 1)
        
        if self.tilt_angle != discretized_angle:
            self.tilt_angle = discretized_angle
            self.needs_redraw = True

    def draw(self):
        """Основна функція для малювання всього на екрані."""
        self.is_drawing = True  # Блокуємо інтерфейс

        self.screen.fill(self.COLOR_BLACK)

        # Малюємо дерево рекурсивно
        self._draw_branch(
            start_pos=self.start_pos,
            angle=self.base_angle,
            length=self.base_length,
            level=self.recursion_level,
            thickness=self.base_thickness
        )

        # Малюємо інтерфейс
        self._draw_ui()

        pygame.display.flip()  # Оновлюємо екран

        self.is_drawing = False  # Розблоковуємо інтерфейс

    def _draw_branch(self, start_pos, angle, length, level, thickness):
        """
        Рекурсивна функція для малювання гілки та її нащадків.

        Args:
            start_pos (tuple): Початкові координати (x, y).
            angle (float): Кут гілки в градусах (-90 = вгору).
            length (float): Довжина гілки.
            level (int): Поточний рівень рекурсії.
            thickness (float): Товщина лінії для гілки.
        """
        if level == 0 or length < 1:
            return

        # Розрахунок кінцевої точки гілки
        angle_rad = math.radians(angle)
        end_x = start_pos[0] + length * math.cos(angle_rad)
        end_y = start_pos[1] + length * math.sin(angle_rad)
        end_pos = (end_x, end_y)

        # Малюємо поточну гілку
        pygame.draw.line(self.screen, self.COLOR_PALE_GREEN, start_pos, end_pos, max(1, int(thickness)))

        # --- Розрахунок параметрів для наступних двох гілок ---

        # Кути розколу відносно поточної гілки
        left_split_angle = 45 - self.tilt_angle
        right_split_angle = 45 + self.tilt_angle

        # Нові абсолютні кути для гілок
        new_angle_left = angle - left_split_angle
        new_angle_right = angle + right_split_angle

        # Нові довжини гілок (за теоремою Піфагора)
        # Коефіцієнт зменшення довжини - cos(кута розколу)
        new_length_left = length * math.cos(math.radians(left_split_angle))
        new_length_right = length * math.sin(math.radians(left_split_angle)) # sin(a) == cos(90-a)

        # Нова товщина (формула для "тюнінгу")
        new_thickness = thickness * 0.80

        # Рекурсивні виклики для лівої та правої гілок
        self._draw_branch(end_pos, new_angle_left, new_length_left, level - 1, new_thickness)
        self._draw_branch(end_pos, new_angle_right, new_length_right, level - 1, new_thickness)

    def _draw_ui(self):
        """Малює всі елементи інтерфейсу."""
        # --- Лічильник рівня рекурсії ---
        label_surf = self.font.render("Рівень рекурсії", True, self.COLOR_WHITE)
        self.screen.blit(label_surf, self.level_label_pos)
        
        value_surf = self.font.render(str(self.recursion_level), True, self.COLOR_GREEN)
        self.screen.blit(value_surf, self.level_value_pos)
        
        pygame.draw.rect(self.screen, self.COLOR_GRAY, self.level_up_button_rect)
        pygame.draw.rect(self.screen, self.COLOR_GRAY, self.level_down_button_rect)
        # Стрілки для кнопок
        pygame.draw.polygon(self.screen, self.COLOR_WHITE, [(self.POS_RX2 + 7, self.POS_RY1 - 3), (self.POS_RX2 + 18, self.POS_RY1 - 3), (self.POS_RX2 + 12.5, self.POS_RY1 - 10)])
        pygame.draw.polygon(self.screen, self.COLOR_WHITE, [(self.POS_RX2 + 7, self.POS_RY1 + 18), (self.POS_RX2 + 18, self.POS_RY1 + 18), (self.POS_RX2 + 12.5, self.POS_RY1 + 25)])

        # --- Повзунок нахилу ---
        label_surf = self.font.render(f"Нахил:", True, self.COLOR_WHITE)
        self.screen.blit(label_surf, self.tilt_label_pos1)
        value_surf = self.font.render(f"{self.tilt_angle}°", True, self.COLOR_GREEN)
        self.screen.blit(value_surf, self.tilt_label_pos2)
        
        # Трек
        pygame.draw.rect(self.screen, self.COLOR_GRAY, self.slider_track_rect, border_radius=5)
        
        # Ручка повзунка
        percentage = (self.tilt_angle + 30) / 60
        handle_x = self.slider_track_rect.x + percentage * self.slider_track_rect.width
        handle_rect = pygame.Rect(0, 0, 12, 20)
        handle_rect.centery = self.slider_track_rect.centery
        handle_rect.centerx = handle_x
        pygame.draw.rect(self.screen, self.COLOR_WHITE, handle_rect, border_radius=3)


# Класичний метод.
# Використовує PyPlot для візуалізації.
def pythagoras_tree_pyplot(recursion_level):
    """
    Малює фрактал "Дерево Піфагора" за допомогою matplotlib.pyplot.

    Ця функція створює статичне зображення дерева. Вона не є інтерактивною.

    Args:
        recursion_level (int): Глибина рекурсії (кількість ітерацій).
        length_reduction_factor (float, optional): Коефіцієнт, на який множиться
            довжина гілки на кожному наступному рівні рекурсії.
            Класичне значення для симетричного дерева - cos(45°), тобто ~0.707.
    """
    # --- Параметри для налаштування візуалізації ---
    BG_COLOR            = 'black'
    BRANCH_COLOR        = 'lightgreen'
    INITIAL_LENGTH      = 100.0  # Початкова довжина стовбура
    INITIAL_THICKNESS   = 5.0    # Початкова товщина стовбура
    THICKNESS_REDUCTION = 0.8    # Коефіцієнт зменшення товщини
    SPLIT_ANGLE         = 45     # Кут розходження гілок (45° для симетричного дерева)
    # Коефіцієнт зменшення довжини згідно з теоремою Піфагора
    LENGTH_REDUCTION_FACTOR = math.cos(math.radians(SPLIT_ANGLE))

    # Створення фігури та осей для малювання
    fig, ax = plt.subplots(figsize=(10, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis('off') # Вимкнути осі координат
    ax.set_aspect('equal', adjustable='box') # Зберегти пропорції

    def _draw_branch_recursive(start_pos, angle, length, level, thickness):
        """
        Вкладена рекурсивна функція для малювання однієї гілки та її нащадків.
        """
        # Базовий випадок: зупиняємо рекурсію, якщо досягли потрібної глибини
        if level == 0:
            return

        # Переводимо кут в радіани для тригонометричних функцій
        angle_rad = math.radians(angle)

        # Розраховуємо координати кінця поточної гілки
        end_x = start_pos[0] + length * math.cos(angle_rad)
        end_y = start_pos[1] + length * math.sin(angle_rad)
        end_pos = (end_x, end_y)

        # Малюємо лінію (гілку) на графіку
        ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]],
                color=BRANCH_COLOR,
                linewidth=max(0.5, thickness))

        # Розраховуємо параметри для двох нових гілок
        new_length = length * LENGTH_REDUCTION_FACTOR
        new_thickness = thickness * THICKNESS_REDUCTION

        # Рекурсивний виклик для лівої гілки
        _draw_branch_recursive(end_pos, angle - SPLIT_ANGLE, new_length, level - 1, new_thickness)
        # Рекурсивний виклик для правої гілки
        _draw_branch_recursive(end_pos, angle + SPLIT_ANGLE, new_length, level - 1, new_thickness)

    # Початковий виклик для стовбура дерева
    # Починаємо з точки (0, -120) і малюємо вгору (кут 90°)
    start_point = (0, -120)
    initial_angle = 90
    _draw_branch_recursive(start_point, initial_angle, INITIAL_LENGTH, recursion_level, INITIAL_THICKNESS)

    # Встановлюємо межі, щоб дерево було видно повністю
    ax.autoscale_view()

    # Показуємо результат
    plt.show()


if __name__ == "__main__":
    # Запуск класичного методу з Matplotlib
    # (закоментуйте да наступні рядки коду, щоб іншу реалізацію, інтерактивну з pygame)

    pythagoras_tree_pyplot(recursion_level=10) # Значення більше 10-12 сповільнює рендеринг
    exit(0)

    # Запуск інтерактивного методу з PyGame
    import pygame

    app = PythagorasTree()
    app.run()