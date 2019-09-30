from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework import generics

from toolkit.pagexml import pagexml_text_region_types
from toolkit.tei_resources import tei_dict

from rules.models import SimpleRule, IgnoreRule
from rules.serializers import SimpleRuleSerializer, IgnoreRuleSerializer


def rules(request):
    context = {"active": "rules"}
    return render(request, "pages/rules/rules.html", context)


def rule_creator(request):
    context = {"active": "rules", "pagexml_types": pagexml_text_region_types, "tei_types": tei_dict}
    return render(request, "pages/rules/rule_creator.html", context)


def rule_browser(request):
    simple_rules = list([model_to_dict(x) for x in list(SimpleRule.objects.all())])
    ignore_rules = list([model_to_dict(x) for x in list(IgnoreRule.objects.all())])
    context = {"active": "rules", "simple": simple_rules, "ignore": ignore_rules}
    return render(request, "pages/rules/rule_browser.html", context)


def create_rule(request, mode):
    post = request.POST

    if mode == "simple":
        try:
            if SimpleRule.objects.filter(name=post["name"]):
                return JsonResponse({"status": "false"}, status=500)

            new_rule = SimpleRule(name=post["name"], base=post["base"], target=post["target"])
            new_rule.save()

            return JsonResponse({"status": "false"}, status=200)
        except:
            return JsonResponse({"status": "false"}, status=500)

    elif mode == "ignore":
        try:
            if SimpleRule.objects.filter(name=post["name"]):
                return JsonResponse({"status": "false"}, status=500)
            new_rule = IgnoreRule(name=post["name"], ignore=post["base"])
            new_rule.save()

            return JsonResponse({"status": "false"}, status=200)
        except:
            return JsonResponse({"status": "false"}, status=500)


def delete_rule(request):
    post = request.POST

    if post["mode"] == "simple":
        remove = SimpleRule.objects.get(name=post["name"])
        remove.delete()

        return JsonResponse({"status": "false"}, status=200)
    elif post["mode"] == "ignore":
        remove = IgnoreRule.objects.get(name=post["name"])
        remove.delete()

        return JsonResponse({"status": "false"}, status=200)


class SimpleRules(generics.ListCreateAPIView):
    queryset = SimpleRule.objects.all()
    serializer_class = SimpleRuleSerializer


class IgnoreRules(generics.ListCreateAPIView):
    queryset = IgnoreRule.objects.all()
    serializer_class = IgnoreRuleSerializer
