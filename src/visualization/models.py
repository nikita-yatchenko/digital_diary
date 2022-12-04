from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Note(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    text = models.CharField(max_length=255, blank=True, null=True)


class Analysis(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    mood = models.CharField(max_length=255, blank=True, null=True)
