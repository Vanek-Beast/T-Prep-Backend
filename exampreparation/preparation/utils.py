from langchain.chat_models import GigaChat
from langchain.prompts import ChatPromptTemplate
from config import api_key
from langchain_core.output_parsers import StrOutputParser


# Основная функция для общения с моделью
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
                                              "Вопрос: {question}"
                                              "Ответ:")
    parser = StrOutputParser()
    llm_chain = prompt | llm | parser
    for question in questions:
        answer = llm_chain.invoke({"question": question})
        answers[question] = answer
    return answers


if __name__ == "__main__":
    questions = [
        "Основные цели и методы государственного регулирования.",
        "Теория общественного выбора. Парадокс Кондорсе и теорема невозможности К.Эрроу.",
        "Макроэкономическое равновесие в модели «AD-AS»."
    ]
    print(generate_answers(questions).values())
