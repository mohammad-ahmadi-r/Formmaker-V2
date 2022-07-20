from django.db import models
import uuid
from django.contrib.auth.models import User


class Form(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Questions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    label = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)

class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)

class ResponseQuestion(models.Model):
    question_id = models.UUIDField()
    response = models.CharField(max_length=255)
    response_id = models.UUIDField()
