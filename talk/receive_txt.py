import socket

def receive_txt():
    HOST = ''
    PORT = 1024
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на {HOST}:{PORT}, ожидает соединения...")
        
        conn, addr = server_socket.accept()
        print(f"Соединение установлено с {addr}")
        
        with conn:
            file_name = "./talk/function.txt"
            with open(file_name, "wb") as f:
                while True:
                    data = conn.recv(1024)  # Получаем данные порциями
                    if not data:  # Если данные закончились
                        break
                    f.write(data)
            print(f"Файл успешно получен и сохранен как {file_name}")