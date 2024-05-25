from django.urls import path

from Home import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home')
]
