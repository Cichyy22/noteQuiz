from django.urls import path
from . import views

urlpatterns = [
    path('proccess_audio/', views.proccess_audio, name='proccess_audio'),
]