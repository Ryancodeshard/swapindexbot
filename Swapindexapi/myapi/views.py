from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets

from .serializers import SwapindexSerializer
from .models import Swapindex


class SwapindexViewSet(viewsets.ModelViewSet):
    queryset = Swapindex.objects.all().order_by('entryId')
    serializer_class = SwapindexSerializer

    def get_queryset(self):
        chatId = self.request.query_params.get('chatId', False)
        courseCode = self.request.query_params.get('courseCode', False)
        currentIndex = self.request.query_params.get('currentIndex', False)
        wantIndex = self.request.query_params.get('wantIndex', False)
        if (courseCode and currentIndex and wantIndex and chatId):
            return Swapindex.objects.filter(courseCode=courseCode) \
                & Swapindex.objects.filter(currentIndex=currentIndex) \
                & Swapindex.objects.filter(wantIndex=wantIndex) \
                & Swapindex.objects.filter(chatId=chatId)
        elif (courseCode and currentIndex and wantIndex):
            return Swapindex.objects.filter(courseCode=courseCode) \
                & Swapindex.objects.filter(currentIndex=currentIndex) \
                & Swapindex.objects.filter(wantIndex=wantIndex)
        elif (courseCode and wantIndex):
            return Swapindex.objects.filter(courseCode=courseCode) \
                & Swapindex.objects.filter(wantIndex=wantIndex)
        elif chatId:
            MyIndex = Swapindex.objects.filter(chatId=chatId)
        else:
            MyIndex = Swapindex.objects.all()
        return MyIndex
