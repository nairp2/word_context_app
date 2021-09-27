from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from word_context_app import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('path', views.path, name='path'),
    #path('result/', views.result, name='json'),
    path('wordquery', views.wordquery, name='wordquery')

]
