import cv2
import numpy as np
import pytesseract
import re
import easyocr
import time

# Укажите путь к Tesseract, если нужно (например, для Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Убедитесь, что путь правильный

def extract_data(text):
    """Извлечение данных из текста с помощью регулярных выражений."""
    data = {}
    # Фамилия Имя Отчество
    fio_match = re.search(r"[А-ЯЁ][а-яё]", text)
    print(123,fio_match)
    data['ФИО'] = fio_match.group(2) if fio_match else "Не найдено"
    
    # Серия и номер паспорта
    passport_match = re.search(r"(\d{4}\s\d{6})", text)
    data['Серия и номер'] = passport_match.group(1) if passport_match else "Не найдено"
    
    # Дата выдачи
    date_match = re.search(r"(\d{2}\.\d{2}\.\d{4})", text)
    data['Дата выдачи'] = date_match.group(1) if date_match else "Не найдено"
    
    # Кем выдан
    issued_by_match = re.search(r"(Кем выдан:.+)", text, re.DOTALL)
    data['Кем выдан'] = issued_by_match.group(1).replace("Кем выдан:", "").strip() if issued_by_match else "Не найдено"
    
    return data

def recognize_with_easyocr(image_path):
    """Распознавание текста с помощью EasyOCR."""
    reader = easyocr.Reader(['ru'], gpu=True)
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)

def passport_main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    image_path = "./photo/passport.jpg"
    cv2.imwrite(image_path, frame)
    camera.release()
    #image_path = "./photo/password.jpg"
    text_easyocr = recognize_with_easyocr(image_path)
    text_easyocr = text_easyocr.replace('\n', ' ')

    sub_str_start = 'ГУ?МВ*'
    res_vrem_start = re.compile(sub_str_start).search(text_easyocr)
    if res_vrem_start == None:
        sub_str_start = 'ОТДЕЛ*'
        res_vrem_start = re.compile(sub_str_start).search(text_easyocr)
        if res_vrem_start == None:
            res_start = ''
        else:
            res_start = str(res_vrem_start.group(0)) 
    else:
        res_start = str(res_vrem_start.group(0))

    raion = ''
    sub_str_end = 'РАЙО*'
    res_vrem_end = re.compile(sub_str_end).search(text_easyocr)
    if res_vrem_end == None:
        sub_str_end = 'ОБЛАС*'
        res_vrem_end = re.compile(sub_str_end).search(text_easyocr)
        if res_vrem_end == None:
            res_end = ''
        else:
            res_end = str(res_vrem_end.group(0)) 
            raion = text_easyocr[text_easyocr.find(res_start):text_easyocr.find(res_end)+7]
            text_easyocr = text_easyocr[text_easyocr.find(res_end)+7:]
    else:
        res_end = str(res_vrem_end.group(0)) 
        raion = text_easyocr[text_easyocr.find(res_start):text_easyocr.find(res_end)+7]
        text_easyocr = text_easyocr[text_easyocr.find(res_end)+7:]

    dates = re.findall(r"(\d{2}\.\d{2}\.\d{4})", text_easyocr)

    for i in dates:
        text_easyocr = text_easyocr.replace(i, '')

    code = ''
    sub_str_code = '...-...'
    res_vrem_code = re.compile(sub_str_code).search(text_easyocr)
    if res_vrem_code == None:
        res_code = ''
    else:
        res_code = str(res_vrem_code.group(0)) 
        code = text_easyocr[text_easyocr.find(res_code):text_easyocr.find(res_code)+7]
        text_easyocr = text_easyocr[text_easyocr.find(res_code)+7:]
    with open('./photo/password_data.txt', 'w', encoding='utf-8') as f:
        f.write(f'{raion};{dates};{code}')

while 1:
    passport_main()
    time.sleep(2)