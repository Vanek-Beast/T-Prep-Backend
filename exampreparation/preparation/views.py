from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SubjectCreateSerializer, SubjectListSerializer
from .models import Subject
from .utils import *


class SubjectCreateView(APIView):
    def post(self, request, user_id):
        data = request.data
        data["user_id"] = user_id
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        data['questions'] = generate_answers(get_questions(uploaded_file))
        serializer = SubjectCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Response({"id": serializer.data["id"]}, status=status.HTTP_201_CREATED)


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