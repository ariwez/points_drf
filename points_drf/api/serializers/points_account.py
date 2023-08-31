from rest_framework import serializers

from points_drf.api.serializers.user import UserSerializer
from points_drf.points.models.points_account import PointsAccount


class PointsAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PointsAccount
        fields = ('user', 'balance',)
        read_only_fields = ('balance',)
