from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    record_id = models.CharField()
    phone_number = models.CharField(max_length=12)
