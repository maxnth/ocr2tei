from django.urls import path, include

from dashboard import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.index, name="index")
]