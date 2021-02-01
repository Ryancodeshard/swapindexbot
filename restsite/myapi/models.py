# models.py

from django.db import models
class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Swapindex(models.Model):
    courseCode = models.CharField(max_length=60)
    currentIndex = models.IntegerField()
    wantIndex = models.IntegerField()
    username = models.CharField(max_length=60)
    chatId = models.IntegerField()

    def __str__(self):
        return self.courseName
