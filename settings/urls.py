from django.urls import path

from settings import views

urlpatterns = [
    path('settings/', views.settings, name="settings"),
    path('settings/<user>', views.settings, name='settings'),
    path('change_editor_theme/', views.change_theme, name='settings'),
]
