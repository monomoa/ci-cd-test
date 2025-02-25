
from django.db import models
from django.contrib.auth.models import User
import os

from uuid import uuid4
from datetime import datetime

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['board/data', ymd_path, uuid_name])

# Create your models here.
class Board(models.Model):
  title = models.CharField(max_length=30)
  content = models.TextField()
  file_upload = models.FileField(upload_to=get_file_path, blank=True)
  filename = models.CharField(max_length=64, null=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  create_date = models.DateTimeField(auto_now_add=True)
  modify_date = models.DateTimeField(auto_now=True, null=True, blank=True)

  def __str__(self):
    return f'[PK:{self.pk}]-{self.title} :: {self.author}'

  def get_absolute_url(self):
    return f'/Board/{self.pk}/'



