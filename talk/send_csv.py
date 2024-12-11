import socket
import csv

def send_csv(file_name, client_socket, BUFFER_SIZE):
    try:
        with open(file_name, "r", encoding="utf-8") as csvfile:
            while True:
                chunk = csvfile.read(BUFFER_SIZE)
                if not chunk:
                    break  # Если данных больше нет, завершаем цикл
                
                client_socket.sendall(chunk.encode("utf-8"))  # Отправляем данные в UTF-8
            
    except:
        with open(file_name, "r", encoding="windows-1251") as csvfile:
            while True:
                chunk = csvfile.read(BUFFER_SIZE)
                if not chunk:
                    break  # Если данных больше нет, завершаем цикл
                
                client_socket.sendall(chunk.encode("windows-1251"))  # Отправляем данные в UTF-8

        

