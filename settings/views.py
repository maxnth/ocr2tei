from django.shortcuts import render
from users.models import CustomUser
from django.http import JsonResponse


def settings(request, user=None):
    context = {"active": "settings"}
    return render(request, "pages/settings.html", context)


def change_theme(request):
    try:
        current_user = CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "false"}, status=500)
    theme = request.POST["theme"]
    current_user.editor_theme = theme
    current_user.save()
    return JsonResponse({"status": "false"}, status=200)
