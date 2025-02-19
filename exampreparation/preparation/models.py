from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=256)
    salt = models.CharField(max_length=256)

    def __str__(self):
        return self.user_name


class Subject(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Segment(models.Model):
    questions = models.JSONField()
    subject_id = models.ForeignKey('Subject', on_delete=models.CASCADE)
    status_segment = models.IntegerField()
    next_review_date = models.DateTimeField(auto_now=True)
