from django.db import models
from django.contrib.auth.models import User
import uuid

class Token(models.Model):
    id = models.UUIDField(default = uuid.uuid4 , primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField()
    
