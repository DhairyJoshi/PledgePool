from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime

# Create your models here.

class pledgepool_user(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    birthdate = models.DateField(default=datetime.date.today)
    # pfp = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    description = models.TextField()