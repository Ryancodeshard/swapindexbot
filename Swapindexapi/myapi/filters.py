from django.contrib.auth.models import Swapindex
import django_filters


class SwapFilter(django_filters.FilterSet):
    class Meta:
        model = Swapindex
        fields = '__all__'
