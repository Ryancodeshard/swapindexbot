from rest_framework import serializers

from .models import Hero, Swapindex

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('id', 'name', 'alias')

class SwapindexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Swapindex
        fields = ('id', 'courseCode', 'currentIndex', 'wantIndex', 'username', 'chatId')