from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
import re


def generate(content):
    # Словарь для хранения вопросов и ответов
    questions_dict = {}

    for line in content.split("\n"):
        # Пропускаем пустые строки
        if not line.strip():
            continue

        # Убираем нумерацию и маркеры списка (-, *, •)
        question = re.sub(r'^(?:\d+[.)]|\s*[-*•])\s*', '', line).strip()

        # Добавляем вопрос и перевёрнутый текст как "ответ"
        questions_dict[question] = question[::-1]

    return questions_dict


class MobileApiView(APIView):
    def post(self, request):
        json = request.data
        # Проверка на наличие всех компонентов
        if all(json.get(key) for key in ['user_id', 'subject_name', 'file_content', 'time']):
            return Response(generate(json.get('file_content')))
        return HttpResponseBadRequest("Bad Request")
