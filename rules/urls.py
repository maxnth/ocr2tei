from django.urls import path
from rules import views

urlpatterns = [
    path('rules/', views.rules, name="export"),
    path('rules/creator/', views.rule_creator, name="creator"),
    path('rules/browser/', views.rule_browser, name="browser"),
    path('rule/create_rule/<mode>/', views.create_rule, name="create"),
    path('rule/delete_rule/', views.delete_rule, name="delete"),
    path('rules/simple_rules/', views.SimpleRules.as_view(), name="simple_rule_list"),
    path('rules/ignore_rules/', views.IgnoreRules.as_view(), name="ignore_rule_list"),
]
