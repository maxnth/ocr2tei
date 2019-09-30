from django.shortcuts import render

from projects import utils


def index(request):
    utils.update_project_list()
    context = {"active": "dashboard"}
    return render(request, "pages/dashboard.html", context)
