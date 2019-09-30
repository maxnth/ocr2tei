from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from projects.serializers import ProjectSerializer
from projects.models import Project, Metadata
from projects.utils import update_project_list, get_pages
from users.models import CustomUser

from django.conf import settings

import os
import shutil


def index(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        context = {"active": "dashboard", "loggedIn": "false"}
        return render(request, "pages/dashboard.html", context)

    context = {"active": "overview"}
    if current_user.loaded_project:
        context["loaded_project"] = current_user.loaded_project
        return render(request, "pages/project/project.html", context)
    else:
        return render(request, "pages/project/project_landing_page.html", context)


def update_projects(request):
    update_project_list()
    return JsonResponse({"status": "false"}, status=200)


def close_project(request):
    current_user = CustomUser.objects.get(id=request.user.id)
    current_user.loaded_project = None
    current_user.loaded_page = None
    current_user.save()
    return JsonResponse({"status": "false"}, status=200)


def delete_project(request, pid):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    try:
        shutil.rmtree((os.path.join(settings.MEDIA_ROOT, "projects", pid)), ignore_errors=True)
        Project.objects.filter(title=pid).delete()
        return JsonResponse({"status": "false"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "false"}, status=500)


def load_project(request, pid, force=False):
    def load():
        current_user.loaded_project = pid

        try:
            current_user.loaded_page = get_pages(pid)[0]["title"]
        except:
            current_user.loaded_page = None

        current_user.save()
        return JsonResponse({"status": "false"}, status=200)

    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    if not Project.objects.get(title=pid):
        return JsonResponse({"status": "false"}, status=500)

    if CustomUser.objects.filter(loaded_project=pid).count():
        if not force:
            return JsonResponse({"status": "false"}, status=500)
        else:
            load()
            return JsonResponse({"status": "false"}, status=200)

    else:
        load()
        return JsonResponse({"status": "false"}, status=200)


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectInfo(ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        try:
            current_user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"status": "false"}, status=404)
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, title=current_user.loaded_project)
        serializer = self.get_serializer(project)
        return Response(serializer.data)


class PageList(APIView):
    def get(self, request, format=None):
        if CustomUser.objects.get(id=request.user.id).loaded_project:
            files = get_pages(CustomUser.objects.get(id=request.user.id).loaded_project)
            return Response(files)


def project_settings(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=200)
    if current_user.loaded_project:
        project = Project.objects.get(title=current_user.loaded_project)
        project.name = request.POST["project_name"]
        project.save()
        return JsonResponse({"status": "false"}, status=200)
    else:
        return JsonResponse({"status": "false"}, status=500)


def project_metadata(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=200)

    project = Project.objects.get(title=current_user.loaded_project)

    metadata = Metadata(project=project,
                        title_statement=request.POST["title_stmt"],
                        edition_statement=request.POST["edition_stmt"],
                        publication_statement=request.POST["publ_stmt"],
                        notes_statement=request.POST["notes_stmt"],
                        source_description=request.POST["source_desc"],
                        series_statement=request.POST["series_stmt"],
                        extent=request.POST["extent"]
                        )
    metadata.save()

    return JsonResponse({"status": "false"}, status=200)
