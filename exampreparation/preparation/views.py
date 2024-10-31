from rest_framework.response import Response
from rest_framework.views import APIView


class MobileApiView(APIView):
    def post(self, request):
        return Response(request.data)  # Возвращаем json, который приходит с мобильного приложения для проверки
