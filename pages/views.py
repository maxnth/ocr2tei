from django.shortcuts import render
from users.models import CustomUser
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
from projects import utils
import toolkit.pagexml as pagexml
import toolkit.tei as tei
from export.utils import save_output

import os
from glob import glob
import json


def page(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        context = {"active": "dashboard", "loggedIn": "false"}
        return render(request, "pages/dashboard.html", context)
    if current_user.loaded_project:
        if current_user.loaded_page:
            tei_elements = tei.get_tei_elements()
            context = {"active": "workflow", "tei_elements": tei_elements}
            return render(request, "pages/page/page.html", context)
        else:
            context = {"active": "overview", "pageSelected": "false"}
            return render(request, "pages/project/project.html", context)
    else:
        context = {"active": "overview"}
        return render(request, "pages/project/project_landing_page.html", context)


def load_page(request, page):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        context = {"active": "dashboard", "loggedIn": "false"}
        return render(request, "pages/dashboard.html", context)
    if current_user.loaded_project:
        current_user.loaded_page = page
        current_user.save()
        return JsonResponse({"status": "false"}, status=200)


def clear_output(request, page):
    current_user = CustomUser.objects.get(id=request.user.id)

    if current_user.loaded_project:
        try:
            os.remove(
                os.path.join(settings.MEDIA_ROOT, "projects", current_user.loaded_project, "output/") + page + ".xml")
            return JsonResponse({"status": "false"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "false"}, status=500)


def delete_page(request, page):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    if current_user.loaded_project:
        try:
            if glob(os.path.join(settings.MEDIA_ROOT, "projects", current_user.loaded_project, "input/") + page + ".*"):
                for file in glob(os.path.join(settings.MEDIA_ROOT, "projects", current_user.loaded_project,
                                              "input/") + page + ".*"):
                    os.remove(file)
            if glob(os.path.join(settings.MEDIA_ROOT, "projects", current_user.loaded_project,
                                 "output/") + page + ".*"):
                for file in glob(os.path.join(settings.MEDIA_ROOT, "projects", current_user.loaded_project,
                                              "output/") + page + ".*"):
                    os.remove(file)
            return JsonResponse({"status": "false"}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"status": "false"}, status=500)


class PageLoader(APIView):
    def get(self, request, format=None):
        try:
            current_user = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            context = {"active": "dashboard", "loggedIn": "false"}
            return render(request, "pages/dashboard.html", context)
        if current_user.loaded_project:
            if current_user.loaded_page:
                page = utils.get_page(current_user.loaded_project, current_user.loaded_page)
                return Response(page)


def set_region_options(request):
    current_user = CustomUser.objects.get(id=request.user.id)

    pid = current_user.loaded_project
    page = current_user.loaded_page
    rid = request.POST["rID"]
    tei_element = request.POST["TEI"]
    ignore = request.POST["Ignore"]

    pagexml.set_region_options(pid, page, rid, element=tei_element, ignore=ignore)
    return JsonResponse({"status": "false"}, status=200)


def set_page_options(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    pid = current_user.loaded_project
    page = current_user.loaded_page
    ignore = request.POST["Ignore"]

    pagexml.set_page_options(pid, page, ignore=ignore)
    return JsonResponse({"status": "false"}, status=200)


def download_page(request):
    post = request.POST

    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    pid = current_user.loaded_project

    pageid = current_user.loaded_page

    save_output(pid, pageid, post["output"])

    return JsonResponse({"status": "false"}, status=200)


def generate_page(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    pid = current_user.loaded_project

    pageid = current_user.loaded_page

    out = tei.generate_page_tei(pid, pageid)

    return JsonResponse({"output": out})
