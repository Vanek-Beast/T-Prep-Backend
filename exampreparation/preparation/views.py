import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import re
from .serializers import SubjectSerializer
from .models import Subject


def generate(file):
    content = file.read().decode('utf-8')
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

    return json.dumps(questions_dict)


class MobileApiView(APIView):
    def post(self, request):
        data = request.data
        # Получаем содержимое файла и генерируем ответы
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        data['questions'] = generate(uploaded_file)
        print(data['questions'])
        serializer = SubjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        post_new = Subject.objects.create(
            user_id=data["user_id"],
            name=data["name"],
            questions=data["questions"]
        )
        return Response({"post": SubjectSerializer(post_new).data}, status=status.HTTP_200_OK)

