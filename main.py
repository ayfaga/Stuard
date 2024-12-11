import subprocess
import sys
python_path = sys.executable

# Запуск файлов параллельно
def run_files_parallel():
    subprocess.Popen([python_path, 'obshee.py'])
    subprocess.Popen([python_path, 'password_function.py'])
    subprocess.Popen([python_path, 'data_talk.py'])

# Запуск параллельного выполнения
if __name__ == "__main__":
    run_files_parallel()
