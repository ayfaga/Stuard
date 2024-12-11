import pygame
import sys
from talk.send_txt import send_file
import pandas as pd
from rapidfuzz import fuzz, process
from collections import Counter
import time
import threading
import random
import subprocess

python_executable = sys.executable

def display_error_message(screen, message, screen_width, screen_height, duration=3000):
    """
    Отображает сообщение об ошибке на экране на несколько секунд.
    :param screen: Pygame Surface для отрисовки
    :param message: Текст сообщения об ошибке
    :param screen_width: Ширина экрана
    :param screen_height: Высота экрана
    :param duration: Длительность отображения в миллисекундах (по умолчанию 3000 мс)
    """
    # Создаём шрифт
    font = pygame.font.SysFont("Times New Roman", 36)
    text_color = (255, 0, 0)  # Красный цвет для ошибки
    background_color = (221, 250, 221)  # Белый фон для сообщения
    
    # Рендер текста
    error_text = font.render(message, True, text_color, background_color)
    text_rect = error_text.get_rect(center=(screen_width // 2, screen_height // 2))
    
    # Отображаем сообщение
    screen.blit(error_text, text_rect)
    pygame.display.flip()
    
    # Ждём указанное время
    pygame.time.delay(duration)
    
def draw_button(screen, x, y, width, height, text, font, button_color, text_color):
    """
    Функция для отрисовки кнопки.
    """
    # Рисуем кнопку
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    
    # Рисуем текст на кнопке
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def input_password_window(screen, font, correct_password, sw, sh):
    """
    Всплывающее окно для ввода пароля администратора.
    """
    # Размеры окна
    window_width, window_height = 600, 250
    window_x = (screen.get_width() - window_width) // 2
    window_y = (screen.get_height() - window_height) // 2
    input_box_color = (255, 255, 255)  # Белый цвет поля ввода
    border_color = (0, 0, 0)  # Черный контур поля ввода
    text_color = (0, 0, 0)  # Цвет текста
    background_color = (200, 200, 200)  # Цвет всплывающего окна
    button_color = (56, 87, 35)
    button_text_color = (255, 255, 255)

    input_box_width, input_box_height = 300, 50
    input_box_x = window_x + (window_width - input_box_width) // 2
    input_box_y = window_y + 60

    attempts = 0  # Счетчик попыток
    password_input = ""  # Введенный текст
    running = True

    while running:
        # Рисуем окно
        pygame.draw.rect(screen, background_color, (window_x, window_y, window_width, window_height))
        pygame.draw.rect(screen, border_color, (window_x, window_y, window_width, window_height), 2)
        
        # Отображение текста
        prompt_text = "Введите пароль администратора:"
        prompt_surface = font.render(prompt_text, True, text_color)
        prompt_rect = prompt_surface.get_rect(center=(window_x + window_width // 2, window_y + 30))
        screen.blit(prompt_surface, prompt_rect)

        # Рисуем поле ввода
        pygame.draw.rect(screen, input_box_color, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, border_color, (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        # Отображение введенного текста
        input_surface = font.render(password_input, True, text_color)
        input_rect = input_surface.get_rect(midleft=(input_box_x + 10, input_box_y + input_box_height // 2))
        screen.blit(input_surface, input_rect)

        # Кнопка "Отправить"
        button_width, button_height = 200, 60
        button_x = window_x + (window_width - button_width) // 2
        button_y = window_y + 130
        draw_button(screen, button_x, button_y, button_width, button_height, "Отправить", font, button_color, button_text_color)

        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Закрытие окна
                    running = False
                elif event.key == pygame.K_BACKSPACE:  # Удаление символа
                    password_input = password_input[:-1]
                elif event.key == pygame.K_RETURN:  # Нажатие Enter
                    if password_input == correct_password:
                        display_error_message(screen, f'Доступ разрешен', sw, sh, duration=800)
                        running = False
                        return True
                    else:
                        attempts += 1
                        if attempts >= 3:
                            display_error_message(screen, f'Доступ запрещен. Превышено количество попыток', sw, sh, duration=800)
                            running = False
                            return False
                        else:
                            display_error_message(screen, f'Неверно. Попробуйте еще раз', sw, sh, duration=800)
                            password_input = ""
            elif event.type == pygame.TEXTINPUT:
                # Обработка ввода текста (подходит для планшета)
                password_input += event.text
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                        if password_input == correct_password:
                            display_error_message(screen, f'Доступ разрешен', sw, sh, duration=800)
                            running = False
                            return True
                        else:
                            attempts += 1
                            if attempts >= 3:
                                display_error_message(screen, f'Доступ запрещен. Превышено количество попыток', sw, sh, duration=800)
                                running = False
                                return False
                            else:
                                print("Ошибка. Попробуйте еще раз.")
                                password_input = ""

def timer():
    global timer_done
    time.sleep(5)  # Ожидание 5 секунд
    timer_done = 1

def input_text_admin(screen, font, text, window_width, window_height):
    """
    Всплывающее окно для ввода пароля администратора.
    """
    # Размеры окна
    window_x = (screen.get_width() - window_width) // 2
    window_y = (screen.get_height() - window_height) // 2
    input_box_color = (255, 255, 255)  # Белый цвет поля ввода
    border_color = (0, 0, 0)  # Черный контур поля ввода
    text_color = (0, 0, 0)  # Цвет текста
    background_color = (200, 200, 200)  # Цвет всплывающего окна
    button_color = (56, 87, 35)
    button_text_color = (255, 255, 255)

    input_box_width, input_box_height = window_width-20, 50
    input_box_x = window_x + (window_width - input_box_width) // 2
    input_box_y = window_y + 60

    text_input = ""  # Введенный текст
    running = True

    while running:
        # Рисуем окно
        pygame.draw.rect(screen, background_color, (window_x, window_y, window_width, window_height))
        pygame.draw.rect(screen, border_color, (window_x, window_y, window_width, window_height), 2)
        
        # Отображение текста
        prompt_text = text
        prompt_surface = font.render(prompt_text, True, text_color)
        prompt_rect = prompt_surface.get_rect(center=(window_x + window_width // 2, window_y + 30))
        screen.blit(prompt_surface, prompt_rect)

        # Рисуем поле ввода
        pygame.draw.rect(screen, input_box_color, (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, border_color, (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        # Отображение введенного текста
        input_surface = font.render(text_input, True, text_color)
        input_rect = input_surface.get_rect(midleft=(input_box_x + 10, input_box_y + input_box_height // 2))
        screen.blit(input_surface, input_rect)

        # Кнопка "Отправить"
        button_width, button_height = 200, 60
        button_x = window_x + (window_width - button_width) // 2
        button_y = window_y + 130
        draw_button(screen, button_x, button_y, button_width, button_height, "Отправить", font, button_color, button_text_color)

        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Закрытие окна
                    running = False
                elif event.key == pygame.K_BACKSPACE:  # Удаление символа
                    text_input = text_input[:-1]
                elif event.key == pygame.K_RETURN:  # Нажатие Enter
                    return text_input
                else:
                    text_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                        return text_input

def main():
    global timer_done
    timer_done = 0
    try:
        df = pd.read_csv('info_pass.csv', encoding="utf-8", sep=";")
    except:
        df = pd.read_csv('info_pass.csv', encoding="windows-1251", sep=";")
    pygame.init()

    # Установка окна на полный экран
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - робот")
    
    # Устанавливаем цвет фона
    background_color = (221, 250, 221)  # RGB цвет
    
    # Цвет квадрата
    square_color = (0, 128, 255)  # Синий (фон квадрата)
    border_color = (0, 0, 0)  # Черный цвет для контура
    border_thickness = 3  # Толщина черного контура

    # Цвет линий, текста и кнопок
    line_color = (0, 0, 0)  # Черный цвет линий
    text_color = (0, 0, 0)  # Черный цвет текста
    button_color = (56, 87, 35)  # Цвет кнопок
    button_text_color = (255, 255, 255)  # Цвет текста кнопок
    # Затираем пароль от злоумышленников
    correct_password = "X"*random.randint(10,50)

    # Отступы
    x_margin = screen_width // 16  # Отступ слева
    y_margin = x_margin  # Отступ сверху и снизу

    # Вычисляем ширину и высоту квадрата
    square_width = screen_width - 2 * x_margin  # Ширина квадрата с учетом отступов
    square_height = square_width * 9 // 7  # Высота квадрата по пропорции 7:9
    
    # Если высота квадрата превышает экран, подгоняем под высоту экрана
    if square_height > screen_height - 2 * y_margin:
        square_height = screen_height - 2 * y_margin
        square_width = square_height * 7 // 9

    # Вычисляем координаты квадрата
    square_x = x_margin  # Позиция по X
    square_y = (screen_height - square_height) // 2  # Центрируем по вертикали между отступами

    # Загрузка изображения
    try:
        image = pygame.image.load("./photo/password_people.png")
        image = pygame.transform.scale(image, (square_width, square_height))  # Масштабируем под размеры квадрата
    except pygame.error:
        print('Ошибка: Не удалось загрузить изображение "./photo/password_people.png"')
        pygame.quit()
        sys.exit()

    # Настройка текста и линий
    font = pygame.font.SysFont("Times New Roman", 40)  # Шрифт для текста
    button_font = pygame.font.SysFont("Times New Roman", 28)  # Шрифт для кнопок

    fio = "Фамилия, Имя, Отчество"
    document = "Наименование документа"
    info_doc= "Информация из документа"
    seat = "Вагон, Место"
    go = "Направление до места"
    labels = [fio, document, info_doc, seat, go]
    inputs = [""] * (len(labels))
    active_input = None
    
    # Параметры для линий
    line_count = len(labels)  # Количество линий
    line_x_start = square_x + square_width  # Начало линии (где заканчивается квадрат)
    line_x_end = screen_width - x_margin  # Конец линии (отступ справа)
    line_length = line_x_end - line_x_start  # Длина линии
    text_offset = 5  # Отступ текста от линии
    
    # Верхняя линия чуть ниже верхней границы квадрата
    line_top_y = square_y + 30  # Отступ от верхней рамки квадрата
    line_bottom_y = square_y + square_height  # Нижняя линия совпадает с нижней рамкой квадрата
    line_spacing = (line_bottom_y - line_top_y) // (line_count - 1)  # Расстояние между линиями

    # Размеры кнопок
    button_width, button_height = 500, 70
    button_margin = 20

    # Координаты кнопок
    left_button_x = x_margin
    left_button_y = screen_height - button_height - button_margin

    right_button_x = screen_width - x_margin - button_width
    right_button_y = left_button_y

    # Основной игровой цикл
    text_fio=''
    text_document=''
    text_info_document=''
    admin_mode = False
    running = True
    while running:
        with open('./talk/function.txt', 'r') as f:
            if f.readline() != '1':
                pygame.quit()  # Корректно завершаем Pygame
                subprocess.Popen([python_executable, "obshee.py"])
                sys.exit()  # Завершаем текущий процесс
        if timer_done == 1:
            timer_done = 0 
            fio = "Фамилия, Имя, Отчество"
            document = "Наименование документа"
            info_doc= "Информация из документа"
            seat = "Вагон, Место"
            go = "Направление до места"
            labels = [fio, document, info_doc, seat, go]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if right_button_x <= event.pos[0] <= right_button_x + button_width and right_button_y <= event.pos[1] <= right_button_y + button_height:
                        if not admin_mode:
                            # Загрузка пароля из файла
                            try:
                                with open("./talk/password.txt", "r") as file:
                                    correct_password = file.read().strip()
                            except FileNotFoundError:
                                print("Ошибка: Файл './talk/password.txt' не найден.")
                                pygame.quit()
                                sys.exit()
                            admin_mode = input_password_window(screen, font, correct_password, screen_width, screen_height)
                        else:
                            if not (text_fio == '' and text_document == '' and text_info_document == ''):
                                A=[]
                                if text_document == '' or text_document.lower() == 'паспорт':
                                    input_text = text_info_document.split()[0]
                                    column_to_search = 'Серия паспорта'
                                    threshold = 95
                                    matches = []
                                    for index, row in df.iterrows():
                                        similarity = fuzz.ratio(input_text.lower(), str(row[column_to_search]).lower())
                                        if similarity >= threshold:
                                            matches.append((index, row[column_to_search], similarity))
                                    if matches:
                                        for match in matches:
                                            A.append(match[0])
                                    input_text = text_info_document.split()[1]
                                    column_to_search = 'Номер паспорта'
                                    threshold = 95
                                    matches = []
                                    for index, row in df.iterrows():
                                        similarity = fuzz.ratio(input_text.lower(), str(row[column_to_search]).lower())
                                        if similarity >= threshold:
                                            matches.append((index, row[column_to_search], similarity))
                                    if matches:
                                        for match in matches:
                                            A.append(match[0])
                                    counter = Counter(A)
                                    most_common_value, most_common_count = counter.most_common(1)[0]
                                    data = df.iloc[most_common_value].tolist()
                                    fio = data[0] + " " + data[1] + " " + data[2]
                                    document = "Паспорт"
                                    info_doc= str(data[3]) + " " + str(data[4])
                                    seat = str(data[8]) + " вагон, " + str(data[9]) + " место"
                                    go = "Направо"
                                    labels = [fio, document, info_doc, seat, go]
                                    threading.Thread(target=timer, daemon=True).start()
                    if left_button_x <= event.pos[0] <= left_button_x + button_width and left_button_y <= event.pos[1] <= left_button_y + button_height:
                        if admin_mode:
                            admin_mode=False
                            text_document=''
                            text_info_document=''
                        else:
                            password = random.randint(100000, 999999)
                            with open('./talk/password.txt', 'w') as f:
                                f.write(str(password))
                            with open('./talk/send.txt', 'w') as f:
                                f.write(f'WAIT_ADMIN {password}')
                                try:
                                    #send_file("./talk/send.txt")
                                    display_error_message(screen, f'Позвал администратора. Ожидайте', screen_width, screen_height, duration=800)
                                    display_error_message(screen, f'Пропустите других пассажиров вперёд. Администратор поможет Вам', screen_width, screen_height, duration=800)
                                except:
                                    display_error_message(screen, f'Ошибка. Попробуйте еще раз', screen_width, screen_height, duration=800)
                    if line_x_start <= event.pos[0] <= line_x_start*3 and line_top_y + 1 * line_spacing <= event.pos[1] <= line_top_y + 1 * line_spacing + 50 and admin_mode:
                        text_document = input_text_admin(screen, font, "Введите наименование документа", 800, 200)
                    if line_x_start <= event.pos[0] <= line_x_start*3 and line_top_y + 2 * line_spacing <= event.pos[1] <= line_top_y + 2 * line_spacing + 50 and admin_mode:
                        text_info_document = input_text_admin(screen, font, "Введите информацию из документа", 1000, 200)
            elif event.type == pygame.KEYDOWN and admin_mode and active_input is not None:
                if event.key == pygame.K_BACKSPACE:
                    inputs[active_input] = inputs[active_input][:-1]
                else:
                    inputs[active_input] += event.unicode
                        
        
        # Заполняем фон
        screen.fill(background_color)

        # Рисуем квадрат с изображением
        screen.blit(image, (square_x, square_y))

        # Рисуем черный контур
        pygame.draw.rect(screen, border_color, (square_x, square_y, square_width, square_height), border_thickness)
        
        if admin_mode==True:
            for i, label in enumerate(labels):
                line_y = line_top_y + i * line_spacing  # Расположение линии по вертикали
                text_surface = font.render(label, True, (0, 0, 0))
                screen.blit(text_surface, (line_x_start, line_top_y + i * line_spacing - 50))
                if 0<i<3:
                    input_box = pygame.Rect(line_x_start, line_top_y + i * line_spacing, line_x_start*1.45, 50)
                    pygame.draw.rect(screen, (255, 255, 255), input_box)
                    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
                    input_text = font.render(inputs[i], True, (0, 0, 0))
                    screen.blit(input_text, (input_box.x + 5, input_box.y + 5))
                else:
                    pygame.draw.line(screen, line_color, (line_x_start, line_y), (line_x_end, line_y), 2)
        # Рисуем линии и текст
        else:
            for i, label in enumerate(labels):
                # Координаты линии
                line_y = line_top_y + i * line_spacing  # Расположение линии по вертикали
                pygame.draw.line(screen, line_color, (line_x_start, line_y), (line_x_end, line_y), 2)
                
                # Рисуем текст над линией
                text_surface = font.render(label, True, text_color)
                text_rect = text_surface.get_rect(midbottom=(line_x_start + line_length // 2, line_y - text_offset))  # Центрируем текст над линией
                screen.blit(text_surface, text_rect)

        input_text_document = font.render(text_document, True, (0, 0, 0))
        screen.blit(input_text_document, (line_x_start + 5, line_top_y + 1 * line_spacing + 5))

        input_text_info_document = font.render(text_info_document, True, (0, 0, 0))
        screen.blit(input_text_info_document, (line_x_start + 5, line_top_y + 2 * line_spacing + 5))
        # Рисуем кнопки
        left_button_text = "Включить режим пользователя" if admin_mode else "Позвать администратора"
        draw_button(screen, left_button_x, left_button_y, button_width, button_height, left_button_text, button_font, button_color, button_text_color)
        right_button_text = "Найти пассажира" if admin_mode else "Ввести пароль администратора"
        draw_button(screen, right_button_x, right_button_y, button_width, button_height, right_button_text, button_font, button_color, button_text_color)
        
        a=[]
        with open('./photo/password_data.txt', 'r', encoding='utf-8') as f:
            a = f.readlines()
        if (a!=[';[];'] and a!= []) and admin_mode==False:
            a=str(a)
            a = a[2:-2]
            a = a.split(";")
            A=[]
            #{raion};{dates};{code}
            input_text = a[0]
            column_to_search = 'Кем выдан'
            threshold = 85
            matches = []
            for index, row in df.iterrows():
                similarity = fuzz.ratio(input_text.lower(), str(row[column_to_search]).lower())
                if similarity >= threshold:
                    matches.append((index, row[column_to_search], similarity))
            if matches:
                for match in matches:
                    A.append(match[0])
            
            input_text = a[1].replace(" ", "") 
            column_to_search = 'Дата выдачи'
            threshold = 85
            matches2 = []
            for index, row in df.iterrows():
                similarity = fuzz.ratio(input_text.lower(), str(row[column_to_search]).lower())
                if similarity >= threshold:
                    matches2.append((index, row[column_to_search], similarity))
            if matches2:
                for match in matches2:
                    A.append(match[0])

            input_text = a[2].replace(" ", "") 
            column_to_search = 'Код подразделения'
            threshold = 80
            matches3 = []
            for index, row in df.iterrows():
                similarity = fuzz.ratio(input_text.lower(), str(row[column_to_search]).lower())
                if similarity >= threshold:
                    matches3.append((index, row[column_to_search], similarity))
            if matches3:
                for match in matches3:
                    A.append(match[0])
            
            counter = Counter(A)
            most_common_value, most_common_count = counter.most_common(1)[0]
            data = df.iloc[most_common_value].tolist()
            fio = data[0] + " " + data[1] + " " + data[2]
            document = "Паспорт"
            info_doc= str(data[3]) + " " + str(data[4])
            seat = str(data[8]) + " вагон, " + str(data[9]) + " место"
            go = "Направо"

            labels = [fio, document, info_doc, seat, go]
            threading.Thread(target=timer, daemon=True).start()
            open('./photo/password_data.txt', 'w').close()
        elif (a!=[';[];'] and a!= []) and admin_mode==True: 
            open('./photo/password_data.txt', 'w').close()
        pygame.display.flip()

    
    # Завершаем работу Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()