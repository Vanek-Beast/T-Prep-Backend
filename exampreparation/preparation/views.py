from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView


class MobileApiView(APIView):
    def post(self, request):
        json = request.data
        # Проверка на наличие всех компонентов
        if all(json.get(key) for key in ['user_id', 'subject_name', 'file', 'time']):
            return Response(json)  # Возвращаем json, который приходит с мобильного приложения для проверки
        return HttpResponseBadRequest("Bad Request")
