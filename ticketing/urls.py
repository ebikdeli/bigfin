from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'ticketing'

router = DefaultRouter()
router.register('ticketings', views.TicketingViewset, 'ticketings')
router.register('answers', views.AnswerViewset, 'answers')
router.register('fileuploads', views.FileUploadViewset, 'fileuploads')

urlpatterns = [
    path('', include(router.urls)),
]
