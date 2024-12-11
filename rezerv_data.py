import socket

with open("./talk/URL_received.txt", "r") as f:
    HOST = f.readline()  # IP-адрес сервера
PORT = 1024  # Тот же порт, который используется сервером

def send_file(file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Соединение с {HOST}:{PORT} установлено")
        A=[]
        with open("./talk/number_robot.txt", "r", encoding='utf-8') as f:
            A.append(f'number_robot = {str(''.join(f.readlines()))}')
        with open("./talk/charge.txt", "r", encoding='utf-8') as f:
            A.append(f'charge = {str(''.join(f.readlines()))}')
        with open("./talk/errors.txt", "r", encoding='utf-8') as f:
            A.append(f'errors = {str(''.join(f.readlines()))}')
        with open("./talk/logs.txt", "r", encoding='utf-8') as f:
            A.append(f'logs = \n{"".join(f.readlines())}')
        with open(file_name, "w", encoding='utf-8') as f:
            f.write("\n".join(A))
        with open(file_name, "rb") as f:
            while chunk := f.read(1024):  # Читаем файл порциями
                client_socket.sendall(chunk)
        print(f"Файл {file_name} успешно отправлен")

if __name__ == "__main__":
    file_name = "./talk/send.txt"  # Имя файла, который вы хотите отправить
    send_file(file_name)
