from rest_framework import serializers
from rules.models import SimpleRule, IgnoreRule


class SimpleRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = SimpleRule
        fields = '__all__'


class IgnoreRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = IgnoreRule
        fields = '__all__'
