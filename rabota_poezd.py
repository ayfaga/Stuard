import pygame
import time
import sys
import subprocess
import os

python_executable = sys.executable

def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def read_orders(file_path):
    """
    Читает данные из файла zakaz.txt и форматирует их в список строк заказа.
    Возвращает список заказов для отображения в таблице.
    """
    orders = []
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            order_num = 1  # Порядковый номер заказа
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue  # Пропускаем некорректные строки

                # Разбираем строку заказа
                vagon = parts[0]
                mesto = parts[1]
                product_data = " ".join(parts[2:-1])  # Продукты с количеством
                status = parts[-1]

                # Если статус "ЗАВЕРШЕНО", пропускаем заказ
                if status == "ЗАВЕРШЕНО":
                    continue

                # Парсим продукты и их количество
                products = product_data.strip("()").split(", ")
                for product in products:
                    name, qty = product.split(" x")
                    orders.append({
                        "num": order_num,
                        "vagon": vagon.replace(',', ''),
                        "mesto": mesto.replace(',', ''),
                        "product": name.strip(),
                        "quantity": qty.strip(),
                        "status": status
                    })
                    order_num += 1
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        sys.exit()

    return orders

def main():
    # Инициализация Pygame
    pygame.init()

    # Получаем размеры экрана
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    # Создаем окно с заданным разрешением
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - заказы")

    # Задаём RGB цвет для фона
    background_color = (221, 250, 221)
    text_color = (0, 0, 0)
    table_border_color = (0, 0, 0)

    # Рассчитываем ширины колонок
    col_widths = [
        1 * screen_width // 8,
        1 * screen_width // 8,
        4 * screen_width // 8,
        2 * screen_width // 8,
    ]

    # Координата X для каждой колонки
    col_positions = [sum(col_widths[:i]) for i in range(len(col_widths))]

    # Рассчитываем высоту каждой строки
    row_height = screen_height // 14

    # Шрифт для текста
    font = pygame.font.SysFont("Times New Roman", 24)
    font_large = pygame.font.SysFont("Times New Roman", 100)  # Для заголовка
    font_medium = pygame.font.SysFont("Times New Roman", 50)  # Для основной информации
    font_small = pygame.font.SysFont("Times New Roman", 30)  # Для таблицы

    # Текущий статус текста
    status_text = "ПОЛУЧЕНО"

    # Время последнего изменения файла
    last_mtime = 0
    file_path = "./talk/zakaz.txt"
    orders = read_orders(file_path)

    # Основной цикл
    running = True
    headers = ["Вагон", "Место", "Продукт", "Количество"]

    while running:
        # Проверяем изменения в файле каждые 2 секунды
        current_mtime = os.path.getmtime(file_path)
        if current_mtime != last_mtime:
            last_mtime = current_mtime
            orders = read_orders(file_path)  # Перезагружаем данные из файла

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем нажатие на текст "ПОЛУЧЕНО"
                mouse_x, mouse_y = event.pos
                if 800 <= mouse_x <= 1200 and 100 <= mouse_y <= 300:
                    # Меняем текст на "СОБРАНО" или обратно
                    cell_text = cell_values[col]
                    text_surface = font.render(cell_text, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(col_x + col_width // 2, row_y + row_height // 2 + screen_height // 2))
                    screen.blit(text_surface, text_rect)
                    status_text = "СОБРАНО" if status_text == "ПОЛУЧЕНО" else "ПОЛУЧЕНО"

        # Заполняем экран заданным цветом
        screen.fill(background_color)

        # Рисуем заголовок "Ожидаю заказа"
        draw_text(screen, "Ожидаю заказа", font_large, text_color, (screen_width // 2 - 350, 20))

        # Рисуем строки и колонки
        for row in range(7):  # Всего 14 строк
            row_y = row * row_height

            # Фон строки
            row_color = (230, 230, 230) if row % 2 == 0 else (255, 255, 255)
            pygame.draw.rect(screen, row_color, (0, row_y + screen_height // 2, screen_width, row_height))

            # Рисуем рамки ячеек
            for col in range(4):  # Всего 6 колонок
                col_x = col_positions[col]
                col_width = col_widths[col]
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # Цвет рамки (чёрный)
                    pygame.Rect(col_x, row_y + screen_height // 2, col_width, row_height),
                    1  # Толщина рамки
                )

                # Если это первая строка, добавляем заголовки
                if row == 0:
                    header_text = headers[col]
                    text_surface = font.render(header_text, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(col_x + col_width // 2, row_y + row_height // 2 + screen_height // 2))
                    screen.blit(text_surface, text_rect)
                else:
                    # Заполняем строки данными заказов
                    order_index = row - 1  # Учитываем, что первая строка — это заголовок
                    if order_index < len(orders):
                        order = orders[order_index]
                        cell_values = [
                            order["vagon"],
                            order["mesto"],
                            order["product"],
                            order["quantity"]
                        ]
                        # Добавляем данные в ячейки строки
                        cell_text = cell_values[col]
                        text_surface = font.render(cell_text, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(col_x + col_width // 2, row_y + row_height // 2 + screen_height // 2))
                        screen.blit(text_surface, text_rect)

        # Рисуем текст ниже слева: "Вагон - ХХ; место - ХХ"
        draw_text(screen, f"Работаю над заказом:", font_medium, text_color, (50, 170))
        draw_text(screen, f"Вагон - {orders[0]['vagon'] if orders else 'N/A'}; место - {orders[0]['mesto'] if orders else 'N/A'}", font_medium, text_color, (50, 240))

        # Рисуем текст "ПОЛУЧЕНО" или "СОБРАНО" справа
        draw_text(screen, status_text, font_medium, text_color, (1000, 200))

        # Обновляем экран
        pygame.display.flip()

        # Задержка на 2 секунды
        time.sleep(2)

    # Корректное завершение работы
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()