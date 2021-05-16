from rest_framework import serializers

from .models import Swapindex


class SwapindexSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Swapindex
        fields = ('entryId', 'courseCode', 'currentIndex',
                  'wantIndex', 'username', 'chatId')
