from rest_framework.serializers import *

from preparation.models import Subject, Segment, User


class SubjectCreateSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class SegmentCreateSerializer(ModelSerializer):
    class Meta:
        model = Segment
        fields = "__all__"


class SubjectListSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'time', 'status']


class SegmentListSerializer(ModelSerializer):
    class Meta:
        model = Segment
        fields = ['id', 'questions', 'subject_id', 'status_segment', 'next_review_date']


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SegmentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Segment
        fields = ['id', 'status_segment', 'next_review_date']


class SegmentDeleteSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class UserGetSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
