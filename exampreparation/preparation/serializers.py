from rest_framework.serializers import *

from preparation.models import *


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
        fields = "__all__"


class SegmentListSerializer(ModelSerializer):
    class Meta:
        model = Segment
        fields = "__all__"


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SegmentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Segment
        fields = ['status_segment', 'next_review_date']


class SegmentDeleteSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class UserGetSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
