from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets

from .serializers import HeroSerializer, SwapindexSerializer
from .models import Hero, Swapindex


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer

class SwapindexViewSet(viewsets.ModelViewSet):
    queryset = Swapindex.objects.all().order_by('courseCode')
    serializer_class = SwapindexSerializer
    def get_queryset(self):
        chatId = self.request.query_params.get('chatId',False)
        courseCode = self.request.query_params.get('courseCode',False)
        if chatId:
            MyIndex = Swapindex.objects.filter(chatId=chatId)
        elif courseCode:
            MyIndex = Swapindex.objects.filter(courseCode=courseCode)
        else:
            MyIndex = Swapindex.objects.all()
        return MyIndex