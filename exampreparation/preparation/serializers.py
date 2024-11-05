from rest_framework.serializers import *


class SubjectSerializer(Serializer):
    user_id = IntegerField()
    name = CharField(max_length=100)
    time = DateTimeField(read_only=True)
    status = BooleanField(default=False)
    questions = JSONField()
