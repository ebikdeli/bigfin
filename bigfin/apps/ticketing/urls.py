from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'ticketing'

router = DefaultRouter()
router.register('ticketing', views.TicketingViewset, 'ticketing')
router.register('answer', views.AnswerViewset, 'answer')
router.register('fileupload', views.FileUploadViewset, 'fileupload')

urlpatterns = [
    path('', include(router.urls)),
]
