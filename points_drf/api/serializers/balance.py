from rest_framework import serializers

from points_drf.points import settings
from points_drf.points.models.points_source import PointsSource


class BalanceSerializer(serializers.Serializer):
    source_key = serializers.CharField(max_length=64, initial=settings.ADMIN_ADD_POINTS_KEY)
    amount = serializers.IntegerField(min_value=1)
    remove_points = serializers.BooleanField(default=False)

    def validate_source_key(self, value):
        """Check if points source exists"""
        if not PointsSource.objects.filter(key=value).exists():
            raise serializers.ValidationError(f'Points source with key: {value} does not exist.')
        return value
