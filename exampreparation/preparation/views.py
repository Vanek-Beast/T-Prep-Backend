import hashlib
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.contrib.sessions.backends.db import SessionStore
from .serializers import *
from .models import *
from .utils import *
import os

session = SessionStore()

class SubjectCreateView(APIView):  # Представление для добавления предмета
    def post(self, request, user_id):
        data = request.data
        data["user_id"] = user_id
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем расширение файла
        allowed_extensions = {'.txt', '.docx', '.doc', '.pdf', '.png', '.jpg', 'jpeg'}  # Разрешенные расширения
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in allowed_extensions:
            return Response(
                {"error": f"Unsupported file type: {file_extension}. Allowed types: {', '.join(allowed_extensions)}."},
                status=status.HTTP_400_BAD_REQUEST)
        match file_extension:
            case '.txt':
                text = get_text_from_txt(uploaded_file.read())
            case '.docx':
                text = get_text_from_docx(uploaded_file.read())
            case '.doc':
                text = get_text_from_doc(uploaded_file.read())
            case '.pdf':
                text = get_text_from_pdf(uploaded_file.read())
            case _:
                text = get_text_from_img(uploaded_file.read())
        questions = generate_answers(extract_questions(text))

        data_subject = {"user_id": data["user_id"], "name": data["name"]}
        serializer_subject = SubjectCreateSerializer(data=data_subject)
        serializer_subject.is_valid(raise_exception=True)
        serializer_subject.save()

        keys = list(questions)
        # Разбиваем на сегменты
        for i in range(0, len(keys), 5):
            questions_load = {k: questions[k] for k in keys[i: i + 5]}
            data_segment = {"questions": questions_load, "subject_id": serializer_subject.data["id"],
                            "status_segment": 0}
            serializer_segment = SegmentCreateSerializer(data=data_segment)
            serializer_segment.is_valid(raise_exception=True)
            serializer_segment.save()
        return Response({"id": serializer_subject.data["id"], "name": serializer_subject.data["name"]},
                        status=status.HTTP_201_CREATED)


class SubjectListView(APIView):  # Представление для получения списка предметов
    def get(self, request, user_id):
        subjects = Subject.objects.filter(user_id=user_id)
        serializer = SubjectListSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SegmentListView(APIView):  # Представление для получения списка сегментов
    def get(self, request, subject_id):
        segments = Segment.objects.filter(subject_id=subject_id)
        serializer = SegmentListSerializer(segments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SegmentUpdateStatusView(APIView):
    def put(self, request, segment_id):
        #получаем сегменты
        segments = Segment.objects.get(id=segment_id)
        serializer = SegmentListSerializer(segments)

        #увеличиваем status на единицу
        date_segment = str(serializer.data['next_review_date']).split('.')[0].replace('T', ' ')
        format_date = "%Y-%m-%d %H:%M:%S"
        date = datetime.strptime(date_segment, format_date)
        status_segment = serializer.data['status_segment']
        status_segment = status_segment + 1
        data_segment = {"status_segment": status_segment}
        serializer_save = SegmentUpdateSerializer(segments, data=data_segment)
        if serializer_save.is_valid():
            serializer_save.save()
            return Response({"status_segment: ": status_segment, "date: ": date}, status=status.HTTP_200_OK)
        return Response({"error": "Недопустимый параметр!"}, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(APIView):  # Представление для регистрации
    def post(self, request):
        data = request.data
        user = User.objects.filter(user_name=data['user_name']).exists()
        if not user:
            salt = generate_salt()
            password = data['user_password']
            if check_password(password):
                password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()
                data_user = {"user_name": data['user_name'], "user_password": str(password), "salt": salt}
                serializer = UserCreateSerializer(data=data_user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"id": serializer.data["user_name"]}, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Пароль не соответствует требованиям!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Пользователь с таким именем уже существует!"}, status=status.HTTP_409_CONFLICT)

class UserAuthView(APIView):  # Представление для авторизации
    def get(self, request, user_name, user_password):
        user = User.objects.filter(user_name=user_name).exists()
        if user:
            user = User.objects.filter(user_name=user_name)
            serializer = UserGetSerializer(user, many=True)
            salt = serializer.data[0]['salt']
            password = user_password
            hash_password = str(hashlib.sha512(password.encode() + salt.encode()).hexdigest())
            if hash_password == serializer.data[0]['user_password']:
                session[f"{serializer.data[0]['id']}"] = serializer.data
                return Response(
                    {"id": session[f"{serializer.data[0]['id']}"][0]['id'], "login": session[f"{serializer.data[0]['id']}"][0]['user_name']},
                    status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Пароль неверный!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Error": "Такого пользователя нет!"}, status=status.HTTP_404_NOT_FOUND)



class UserLogoutView(APIView):
    def post(self, request, user_id):
        if f'{user_id}' in session:
            del session[f'{user_id}']
            return Response({"Answer": "Вы вышли из системы!"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Вы еще не авторизовались!"}, status=status.HTTP_404_NOT_FOUND)


class SubjectDeleteView(APIView):  # Представление для удаления предмета
    def delete(self, request, user_id, subject_id):
        subject = get_object_or_404(Subject, id=subject_id, user_id=user_id)
        subject.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class QuestionUpdateView(APIView):  # Представление для изменения ответа на вопрос
    def patch(self, request, segment_id):
        # Получаем сегмент
        segment = get_object_or_404(Segment, id=segment_id)

        # Загружаем вопросы из сегмента
        serializer = SegmentListSerializer(segment)
        quest_dict = serializer.data["questions"]
        # Проверяем наличие вопроса в запросе
        if "question" in request.data and "answer" in request.data:
            question_key = request.data["question"]

            # Обновляем ответ на указанный вопрос
            if question_key in quest_dict:
                quest_dict[question_key] = request.data["answer"]

                # Сохраняем измененный словарь вопросов обратно в сегмент
                segment.questions = quest_dict
                segment.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": f"Вопрос '{question_key}' не найден."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Не указаны необходимые параметры 'question' и/или 'answer'."},
                            status=status.HTTP_400_BAD_REQUEST)
