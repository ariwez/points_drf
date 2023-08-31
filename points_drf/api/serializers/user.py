from rest_framework import serializers

from points_drf.points.models.user import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'referrer_email',)
