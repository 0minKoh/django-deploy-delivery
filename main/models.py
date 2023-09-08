from django.db import models

# Create your models here.
class Main(models.Model):
  ip = models.CharField(max_length=50)
  url = models.CharField(max_length=200)

def __str__(self):
  return self
