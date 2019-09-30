from rest_framework import serializers
from projects.models import Project, Metadata


class MetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Metadata
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    last_edit = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    metadata = MetadataSerializer(read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
