from django_filters import rest_framework as filters

from .models import Ticketing, Answer, FileUpload


class TicketingFilterSet(filters.FilterSet):
    """Filterset for Ticketing model"""

    class Meta:
        model = Ticketing
        fields = '__all__'


class AnswerFilterSet(filters.FilterSet):
    """Filterset for Anwer Model"""

    class Meta:
        model = Answer
        fields = '__all__'


class FileUploadFilterSet(filters.FilterSet):
    """Filterset for FileUpload Model"""

    class Meta:
        model = FileUpload
        exclude = ['file', ]
