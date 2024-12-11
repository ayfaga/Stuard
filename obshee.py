import pygame
import os
import time
from talk.receive_csv import receive_csv
from talk.receive_txt import receive_txt
from talk.send_txt import send_file
import sys
import subprocess

python_executable = sys.executable

def main():
    # Инициализация Pygame
    pygame.init()

    # Установка окна на полный экран
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - данные")

    # Цвет фона
    background_color = (221, 250, 221)

    # Шрифт для текста
    font = pygame.font.SysFont("Times New Roman", 48)
    text_color = (0, 0, 0)

    # Основной цикл программы
    running = True
    while running:
        # Проверка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Завершение программы
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Закрытие программы по клавише Esc
                    running = False

        # Проверяем наличие файла info_pass.csv
        if os.path.exists("./info_pass.csv"):
            # Проверяем значение в файле ./talk/function.txt
            if os.path.exists("./talk/function.txt"):
                try:
                    with open("./talk/function.txt", "r", encoding = 'utf-8') as f:
                        function_value = f.read().strip()
                except:
                    function_value='0'
                if function_value == "1":
                    pygame.quit()  # Корректно завершаем Pygame
                    subprocess.Popen([python_executable, "skan_passport.py"])
                    sys.exit()  # Завершаем текущий процесс
                    message = "Включена функция проверки паспорта"
                elif function_value == "2":
                    message = "Включена функция работы внутри вагона"
                    pygame.quit()  # Корректно завершаем Pygame
                    subprocess.Popen([python_executable, "rabota_poezd.py"])
                    sys.exit()  # Завершаем текущий процесс
                else:
                    message = "Ожидаю дальнейших функций"
                    screen.fill(background_color)
                    # Рендеринг текста
                    text_surface = font.render(message, True, text_color)
                    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    receive_txt()
            else:
                message = "Ожидаю дальнейших функций"
                screen.fill(background_color)
                # Рендеринг текста
                text_surface = font.render(message, True, text_color)
                text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                receive_txt()
        else:
            message = "Ожидаю файл info_pass.csv из сервера"
            # Заливка экрана фоновым цветом
            screen.fill(background_color)

            # Рендеринг текста
            text_surface = font.render(message, True, text_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            receive_csv("./info_pass.csv")
            f=open('./info_pass.csv', 'r') 
            try:
                a=f.read(1)
                if a == '1' or a == '2':
                    with open('./talk/send.txt', 'w') as f:
                        f.write('NO_CSV')
                    send_file("./talk/send.txt")
                f.close()
                os.remove("./info_pass.csv")
            except:
                continue
            


        # Заливка экрана фоновым цветом
        screen.fill(background_color)

        # Рендеринг текста
        text_surface = font.render(message, True, text_color)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)

        # Обновление экрана
        pygame.display.flip()

        # Небольшая задержка, чтобы избежать высокой нагрузки на процессор
        time.sleep(0.1)

    # Завершение работы Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
