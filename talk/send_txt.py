import socket

def send_file(file_name):
    with open("./talk/URL_received.txt", "r") as f:
        HOST = f.readline()  # IP-адрес сервера
    PORT = 1024  # Тот же порт, который используется сервером
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Соединение с {HOST}:{PORT} установлено")
        
        with open(file_name, "rb") as f:
            while chunk := f.read(1024):  # Читаем файл порциями
                client_socket.sendall(chunk)
        print(f"Файл {file_name} успешно отправлен")

if __name__ == "__main__":
    file_name = "./talk/send.txt"  # Имя файла, который вы хотите отправить
    send_file(file_name)
