# models.py

from django.db import models


class Swapindex(models.Model):
    entryId = models.AutoField(primary_key=True)
    courseCode = models.CharField(max_length=60)
    currentIndex = models.IntegerField()
    wantIndex = models.IntegerField()
    username = models.CharField(max_length=60)
    chatId = models.IntegerField()

    def __str__(self):
        return self.username
