from langchain_gigachat.chat_models import GigaChat
from config import api_key


# Функция для создания экземпляра GigaChat
def create_llm(api_key):
    return GigaChat(
        credentials=api_key,
        scope="GIGACHAT_API_PERS",
        model="GigaChat",
        verify_ssl_certs=False,
        streaming=False,
    )


# Основная функция для общения с моделью
def generate_answers(llm, questions):
    answers = {}
    # Добавляем системное сообщение с начальной настройкой, если оно задано
    prompt = "Ты - эксперт по подготовке к экзаменам. Тебе будет дан вопрос, " \
             "на который необходимо дать краткий и точный ответ, учитывая каждый пункт, " \
             "указанный в вопросе.В ответе необходимо отдать перевод в формате, приведенном ниже." \
             "Ты ДОЛЖЕН дать четкий ответ на вопрос."
    llm.invoke(prompt)
    for question in questions:
        answer = llm.invoke(question)
        answers[question] = answer.content
    return answers


if __name__ == "__main__":
    llm = create_llm(api_key)
    questions = [
        "Электрическое поле в вакууме. Напряженность электростатического поля. Принцип суперпозиции.",
        "Электрический диполь. Напряженность поля на оси диполя.",
        "Электрический диполь. Напряженность поля диполя на оси, лежащей на перпендикуляре, восстановленном к его середине.",
        "Поток вектора напряженности. Теорема Остроградского-Гаусса."
    ]
    print(generate_answers(llm, questions))
