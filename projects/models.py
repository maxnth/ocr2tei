from django.db import models
from datetime import datetime


class Project(models.Model):
    title = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, default=None, null=True)
    pages = models.IntegerField(default=0)
    creation_time = models.DateTimeField(auto_now_add=True, null=True)
    last_edit = models.DateTimeField(default=datetime.now, null=True)
    percent_corrected = models.DecimalField(max_digits=4, decimal_places=2, default=0)


class Metadata(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)

    title_statement = models.CharField(max_length=255, default=None, null=True)
    edition_statement = models.CharField(max_length=255, default=None, null=True)
    notes_statement = models.CharField(max_length=255, default=None, null=True)
    publication_statement = models.CharField(max_length=255, default=None, null=True)
    series_statement = models.CharField(max_length=255, default=None, null=True)
    source_description = models.CharField(max_length=255, default=None, null=True)
    extent = models.CharField(max_length=255, default=None, null=True)
