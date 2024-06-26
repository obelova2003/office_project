import django_filters
from django_filters.rest_framework import FilterSet

from api.models import Application, OfficeUser

class ApplicationFilter(FilterSet):
    author_client = django_filters.ModelMultipleChoiceFilter(queryset=OfficeUser.objects.all(),)

    class Meta:
        model = Application
        fields = ['author_client', ]