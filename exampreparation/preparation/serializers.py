from rest_framework.serializers import *

from preparation.models import Subject


class SubjectCreateSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectListSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
