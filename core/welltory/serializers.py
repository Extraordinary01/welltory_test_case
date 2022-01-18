from rest_framework import serializers
from .models import Correlation


class CorrelationValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correlation
        fields = ("value", "p_value")


class CorrelationSerializer(serializers.ModelSerializer):
    correlation = serializers.SerializerMethodField()
    x_data_type = serializers.StringRelatedField(read_only=True)
    y_data_type = serializers.StringRelatedField(read_only=True)

    def get_correlation(self, obj):
        return CorrelationValueSerializer(obj).data

    class Meta:
        model = Correlation
        fields = ("user_id", "x_data_type", "y_data_type", "correlation")
