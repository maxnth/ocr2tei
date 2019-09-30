from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import JsonResponse

from users.models import CustomUser
from rules.models import SimpleRule, IgnoreRule
from export import utils
from toolkit.tei import build_tei


def export_results(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        context = {"active": "dashboard", "loggedIn": "false"}
        return render(request, "pages/dashboard.html", context)

    if current_user.loaded_project:
        if current_user.loaded_page:
            simple_rules = list([model_to_dict(x) for x in list(SimpleRule.objects.all())])
            ignore_rules = list([model_to_dict(x) for x in list(IgnoreRule.objects.all())])
            context = {"active": "export", "simple": simple_rules, "ignore": ignore_rules}
            return render(request, "pages/export.html", context)
        else:
            context = {"active": "overview", "pageSelected": "false"}
            return render(request, "pages/project/project.html", context)

    else:
        context = {"active": "overview"}
        return render(request, "pages/project/project_landing_page.html", context)


def download_export(request):
    post = request.POST

    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    pid = current_user.loaded_project

    utils.save_output(pid, text=post["output"])

    return JsonResponse({"status": "false"}, status=200)


def generate_export(request):
    post = request.POST

    pages = post.getlist("page[]", False)

    if not pages:
        return JsonResponse({"status": "false"}, status=500)

    simple_rules = post.getlist("simple_rule[]", False)
    ignore_rules = post.getlist("ignore_rule[]", False)

    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)

    pid = current_user.loaded_project

    out = build_tei(pid, pages, simple_rules, ignore_rules)

    return JsonResponse({"output": out})
