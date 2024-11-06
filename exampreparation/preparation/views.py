import json

from django.shortcuts import get_object_or_404
from rest_framework import status, generics
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


class SubjectCreateView(APIView):
    def post(self, request, user_id):
        data = request.data
        data["user_id"] = user_id
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        data['questions'] = generate(uploaded_file)
        serializer = SubjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data}, status=status.HTTP_200_OK)


class SubjectListView(APIView):
    def get(self, request, user_id):
        # Получаем список предметов для конкретного пользователя
        subjects = Subject.objects.filter(user_id=user_id)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectDetailView(APIView):
    def get(self, request, user_id, subject_id):
        # Получаем предмет по subject_id для конкретного пользователя
        subject = get_object_or_404(Subject, id=subject_id, user_id=user_id)
        return Response({"questions": subject.questions}, status=status.HTTP_200_OK)