from django.urls import path
from export import views

urlpatterns = [
    path('project/export/', views.export_results, name="export"),
    path('download_export/', views.download_export, name="download"),
    path('generate_export/', views.generate_export, name="generate"),
]
