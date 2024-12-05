import os
import re
import random
import numpy as np
import pytesseract
import cv2
from langchain_community.chat_models import GigaChat
from langchain.prompts import ChatPromptTemplate
from .config import api_key
from langchain_core.output_parsers import StrOutputParser
from docx import Document
from io import BytesIO
from PyPDF2 import PdfReader
import subprocess


# Основная функция для получения ответов на вопросы
def generate_answers(questions):
    answers = {}
    llm = GigaChat(
        credentials=api_key,
        scope="GIGACHAT_API_PERS",
        model="GigaChat",
        verify_ssl_certs=False,
        streaming=False,
    )
    prompt = ChatPromptTemplate.from_template("Ты - эксперт по подготовке к экзаменам. "
                                              "Тебе будет дан вопрос, на который необходимо дать краткий и точный "
                                              "ответ, учитывая каждый пункт, указанный в вопросе."
                                              "Ты ДОЛЖЕН дать четкий ответ на вопрос."
                                              "Если вопрос задан на английском языке, то и ответ давай на английском!"
                                              "Вопрос: {question}"
                                              "Ответ:")
    parser = StrOutputParser()
    llm_chain = prompt | llm | parser
    for question in questions:
        answer = llm_chain.invoke({"question": question})
        answers[question] = answer
    return answers


# Функция для получения текста из txt файла
def get_text_from_txt(file_content):
    return file_content.decode('utf-8')


# Функция для разбиения на отдельные вопросы и очистки их от ненужных символов
def crop_questions(content):
    # Список для хранения вопросов
    questions = []

    for line in content.split("\n"):
        # Пропускаем пустые строки
        if not line.strip():
            continue

        # Убираем нумерацию и маркеры списка (-, *, •)
        question = re.sub(r'^(?:\d+[.)]|\s*[-*•])\s*', '', line).strip()

        questions.append(question)

    return questions


# Функция для получения текста из изображений
def get_text_from_img(img):
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' нужно для Windows
    # Декодируем байтовое содержимое в изображение
    file_bytes = np.frombuffer(img, np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Применение OCR
    text = pytesseract.image_to_string(gray, lang='rus')
    return text


# Функция для получения текста из docx файлов
def get_text_from_docx(file_content):
    # Создаем объект BytesIO из байтового содержимого
    file_stream = BytesIO(file_content)

    # Открываем docx файл из потока
    doc = Document(file_stream)

    # Извлекаем текст из каждого параграфа
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text


# Функция для получения текста из doc файлов
def get_text_from_doc(file_bytes, output_path="decoded_file.doc"):
    # Сохраняем байты в файл
    with open(output_path, "wb") as f:
        f.write(file_bytes)
    # Извлекаем текст с помощью antiword
    result = subprocess.run(['antiword', output_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    os.remove(output_path)
    return result.stdout


# Функция для получения текста из pdf
def get_text_from_pdf(file_content):
    # Создаем объект BytesIO из байтового содержимого
    file_stream = BytesIO(file_content)

    # Создаем объект PdfReader
    reader = PdfReader(file_stream)

    # Извлекаем текст из всех страниц
    all_text = []
    for page in reader.pages:
        all_text.append(page.extract_text())

    return "\n".join(all_text)


# Функция для извлечения вопросов из текста
def extract_questions(text):
    llm = GigaChat(
        credentials=api_key,
        scope="GIGACHAT_API_PERS",
        model="GigaChat",
        verify_ssl_certs=False,
        streaming=False,
    )
    prompt = ChatPromptTemplate.from_template('''
        Тебе предоставлен текст. Извлеки из него только те строки, которые являются вопросами для подготовки к экзаменам. 

        **Важно:**
        - **Не оставляй в выводе**: 
            - Нумерацию (например, 1., 2.), списочные маркеры (-, • и т.д.).
            - Заголовки, текст вне вопросов или случайный текст.
            - Любые дополнительные символы, форматирование или исправления.
        - **Не изменяй смысл вопросов, но исправь грамматические ошибки, вызванные некорректным считыванием текста.**:
            - Не придумывай свои вопросы.
            - Не изменяй формулировки, порядок слов или структуру вопросов.
            - Если вопрос состоит из нескольких предложений, сохраняй его целиком в одной строке.
            - В тексте могут содержаться опечатки или некорректная маркировка вопросов, но ты всё равно должен взять их и ничего не пропустить.
        - **Каждый вопрос возвращай с новой строки, без лишнего текста или форматирования**.

        **Пример 1:**
        Текст:
        «Экономика. Вопросы к экзамену.».
        1. Фиаско рынка и необходимость государственного регулирования экономики.
        2. Теория общественного выбора. Парадокс Кондорсе и теорема невозможности К. Эрроу.
        3. Основные цели и методы государственного регулирования.

        Ответ:
        Фиаско рынка и необходимость государственного регулирования экономики.
        Теория общественного выбора. Парадокс Кондорсе и теорема невозможности К. Эрроу.
        Основные цели и методы государственного регулирования.

        **Пример 2 (с опечатками):**
        Текст:
        Физика: Вопрсы для экзаменов.
        1. Электический заряад, его свойства. 
        2. Элктрическое поле в вакууме. Напряженность электростатического поля. Принцип суперпозиции.
        3. Элктрический диполь. Напряженность поля диполя на оси, лежащей на перпендикуляре, восстановленном к его середине.

        Ответ:
        Электрический заряд, его свойства.
        Электрическое поле в вакууме. Напряженность электростатического поля. Принцип суперпозиции.
        Электрический диполь. Напряженность поля диполя на оси, лежащей на перпендикуляре, восстановленном к его середине.

        Теперь извлеки вопросы для подготовки к экзаменам из следующего текста, при необходимости исправив грамматические ошибки, не пропусти ни одного вопроса!!!:
        {text}
        ''')

    parser = StrOutputParser()

    # Подключаем цепочку
    llm_chain = prompt | llm | parser

    # Получаем ответ
    answer = llm_chain.invoke({"text": text})

    return crop_questions(answer)


def generate_salt():
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = []

    for i in range(16):
        chars.append(random.choice(alphabet))

    return "".join(chars)


def check_password(password):
    val = True
    if len(password) < 8 or len(password) > 24:
        val = False
    elif set('[~!@#$%^&*()_+{}":;\']+$').intersection(password):
        val = False

    return val
