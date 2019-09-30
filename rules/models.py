from django.db import models


class SimpleRule(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    base = models.CharField(max_length=255)
    target = models.CharField(max_length=255)


class IgnoreRule(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    ignore = models.CharField(max_length=255)
