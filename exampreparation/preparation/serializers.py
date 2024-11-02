from rest_framework import serializers


class SubjectSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    time = serializers.DateTimeField(read_only=True)
    status = serializers.BooleanField(default=False)
    file = serializers.JSONField()
