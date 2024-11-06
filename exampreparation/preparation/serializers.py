from rest_framework.serializers import *

from preparation.models import Subject


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ("name", "id")
