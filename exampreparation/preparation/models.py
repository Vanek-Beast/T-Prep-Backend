from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_password = models.CharField(max_length=64)

    def __str__(self):
        return self.user_name


class Subject(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    file = models.JSONField()

    def __str__(self):
        return self.name
