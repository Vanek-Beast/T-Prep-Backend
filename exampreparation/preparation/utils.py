import json
import re
import numpy as np
import pytesseract
import cv2
from langchain_community.chat_models import GigaChat
from langchain.prompts import ChatPromptTemplate
from config import api_key
from langchain_core.output_parsers import StrOutputParser


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
    return json.dumps(answers)


# Функция для получения содержимого файла из байтов
def get_content(file):
    return file.read().decode('utf-8')


# Функция для получения вопросов из файла
def get_questions(content):
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


def get_text_from_img(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Декодируем байтовое содержимое в изображение
    file_bytes = np.frombuffer(img, np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Применение OCR
    text = pytesseract.image_to_string(gray, lang='rus+eng')
    return text
