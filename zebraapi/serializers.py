from rest_framework import serializers
from .models import ZebraQuery, ZebraResult

class ZebraResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZebraResult
        fields = ['id', 'source', 'data', 'fetched_at']

class ZebraQuerySerializer(serializers.ModelSerializer):
    reults = ZebraResultSerializer(many=True, read_only=True)
    class Meta:
        model = ZebraQuery
        fields = ['id', 'input_value', 'input_type', 'for_education', 'consent_given', 'created_at', ' results' ]

