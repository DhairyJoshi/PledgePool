from django.db import models
from django.contrib.postgres.fields import ArrayField
import datetime

# Create your models here.
def upload_to_pfps(instance, filename):
    return f'pfps/{instance.username}/{filename}'

class pledgepool_user(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    birthdate = models.DateField(default=datetime.date.today)
    pfp = models.ImageField(upload_to=upload_to_pfps, blank=True, null=True)
    description = models.TextField()