from django.contrib import admin
from django.urls import path, include


from pages import views

urlpatterns = [
    path('project/page/', views.page, name="index"),
    path('load_page/<page>', views.load_page, name="load_page"),
    path('loaded_page/', views.PageLoader.as_view(), name="loaded_page"),
    path('clear_output/<page>', views.clear_output, name="clear_output"),
    path('delete_page/<page>', views.delete_page, name="delete_page"),
    path('set_region_tei/', views.set_region_options, name="set_region_tei"),
    path('set_page_options/', views.set_page_options, name="set_page_options"),
    path('download_page/', views.download_page, name="download_page"),
    path('generate_page_output/', views.generate_page, name="generate_page_output"),
]
