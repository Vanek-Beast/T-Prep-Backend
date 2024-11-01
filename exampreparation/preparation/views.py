from django.http import HttpResponseBadRequest
from rest_framework import status
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
        data = request.data

        # Проверка на наличие всех необходимых полей
        required_fields = ['user_id', 'subject_name', 'file_content', 'time']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response(
                {"error": f"Missing fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем содержимое файла и генерируем ответы
        file_content = data.get('file_content')

        return Response(generate(file_content), status=status.HTTP_200_OK)

