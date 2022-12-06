from django.db import models
from django.contrib.auth.models import User
import pandas as pd
from datetime import datetime
import pytz
# Create your models here.


class DiaryEntry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    sentiment_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=
                                      datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = models.DateTimeField(auto_now_add=
                                      datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S'))

    def __str__(self):
        return self.title + "\n" + self.text

    @staticmethod
    def get_dataset():
        return pd.DataFrame(DiaryEntry.objects.all().values())
