import vosk
import pyaudio
import time
import pyttsx3
from transliterate import translit

# Инициализация голосового движка
tts_engine = pyttsx3.init()

# Список вариантов активации
activation_commands = ["туту", "ту-ту", "ту ту", "тут", "тю-тю", "тутту", "тутуту", "тату", "тыту"]

# Функция для преобразования текста в речь
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Функция для прослушивания и распознавания речи
def listen():
    model = vosk.Model("vosk-model-small-ru-0.22")  # Убедитесь, что у вас скачана модель vosk
    recognizer = vosk.KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Слушаю...")
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)['text']
            return text.lower()

# Функция для обработки текста и приведения его к кириллице
def process_text(text):
    try:
        text_cyrillic = translit(text, 'ru')
        print(f"Вы сказали: {text_cyrillic}")
        return text_cyrillic.lower()
    except Exception:
        print(f"Вы сказали: {text}")
        return text.lower()

# Главная функция
def main():
    active = False  # Флаг активности ассистента
    while True:
        text = listen()
        text = process_text(text)
        words = text.strip().split()
        
        if not active:
            if text in activation_commands:
                active = True
                speak("Я вас слушаю.")
            else:
                continue
        else:
            if words == ["стоп"] or words == ["спасибо"]:
                active = False
                speak("Рад помочь!")
                continue
            else:
                if text == "":
                    continue  # Молчание, ничего не говорим
                elif "расписание поездов" in text:
                    response = "Вы можете узнать расписание поездов на официальном сайте РЖД."
                elif "основана компания" in text:
                    response = "Компания российские железные дороги основана девятого июля две тысячи третьего года"
                elif "купить билет" in text:
                    response = "Билеты можно приобрести в кассах вокзала или онлайн через приложение РЖД."
                else:
                    response = "Повторите вопрос."
                speak(response)

if __name__ == "__main__":
    time.sleep(1)
    speak("Я вас слушаю.")
    time.sleep(1)
    speak("Компания российские железные дороги основана девятого июля две тысячи третьего года")
    time.sleep(1)
    speak("Рад помочь!")