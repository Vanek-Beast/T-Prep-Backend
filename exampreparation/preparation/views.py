import json

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import re
from .serializers import *
from .models import *


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

        questions = generate(uploaded_file)
        questions_dict = json.loads(questions)

        data_subject = {"user_id": data["user_id"], "name": data["name"]}
        serializer_subject = SubjectCreateSerializer(data=data_subject)
        serializer_subject.is_valid(raise_exception=True)
        serializer_subject.save()

        keys = list(questions_dict)
        for i in range(0, len(keys), 5):
            questions_load = {k: questions_dict[k] for k in keys[i: i + 5]}
            questions_load = json.dumps(questions_load)
            data_segment = {"questions": questions_load, "subject_id": serializer_subject.data["id"], "status_segment": 0}
            serializer_segment = SegmentCreateSerializer(data=data_segment)
            serializer_segment.is_valid(raise_exception=True)
            serializer_segment.save()

        return Response({"id": serializer_subject.data["id"], "name": serializer_subject.data["name"]},
                        status=status.HTTP_201_CREATED)


class SubjectListView(APIView):
    def get(self, request, user_id):
        # Получаем список предметов для конкретного пользователя
        subjects = Subject.objects.filter(user_id=user_id)
        serializer = SubjectListSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectDetailView(APIView):
    def get(self, request, user_id, subject_id):
        # Получаем предмет по subject_id для конкретного пользователя
        subject = get_object_or_404(Subject, id=subject_id, user_id=user_id)
        return Response({"questions": subject.questions}, status=status.HTTP_200_OK)


class SegmentListView(APIView):
    def get(self, request, subject_id):
        segments = Segment.objects.filter(subject_id=subject_id)
        serializer = SegmentListSerializer(segments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    def post(self, request, user_name, user_password):
        data = request.data
        data["user_name"] = user_name
        data["user_password"] = user_password
        serializer = UserCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"id": serializer.data["id"]}, status=status.HTTP_201_CREATED)


class SegmentUpdateView(APIView):
    def patch(self, request, segment_id):
        segment = get_object_or_404(Segment, id=segment_id)
        serializer = SegmentUpdateSerializer(segment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(code=201, data=serializer.data)
        return JsonResponse(code=400, data="wrong parameters")
