import json
import re

from langchain.chat_models import GigaChat
from langchain.prompts import ChatPromptTemplate
from .config import api_key
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


# Функция для получения вопросов из файла
def get_questions(file):
    content = file.read().decode('utf-8')
    # Словарь для хранения вопросов и ответов
    questions = []

    for line in content.split("\n"):
        # Пропускаем пустые строки
        if not line.strip():
            continue

        # Убираем нумерацию и маркеры списка (-, *, •)
        question = re.sub(r'^(?:\d+[.)]|\s*[-*•])\s*', '', line).strip()

        questions.append(question)

    return questions
