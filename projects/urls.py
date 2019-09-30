from django.contrib import admin
from django.urls import path, include

from projects import views

urlpatterns = [
    path('project/', views.index, name='index'),
    path('project_info/', views.ProjectInfo.as_view({"get": "list"}), name="Project Info"),
    path('update_projects/', views.update_projects, name="update_projects"),
    path('delete_project/<pid>', views.delete_project, name="delete_project"),
    path('close_project/', views.close_project, name="close_project"),
    path('load_project/<pid>', views.load_project, name="load_project"),
    path('load_project/<str:pid>/<int:force>', views.load_project, name="load_project"),
    path('project_list/', views.ProjectList.as_view(), name="project_list"),
    path('project_page_list/', views.PageList.as_view(), name="page_list"),
    path('project_settings/', views.project_settings, name="project_settings"),
    path('project_metadata/', views.project_metadata, name="project_metadata"),
]
