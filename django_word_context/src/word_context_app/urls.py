from django.contrib import admin
from django.urls import path, include
from word_context_app import views

urlpatterns = [
    path('', views.home, name='home'),
]
