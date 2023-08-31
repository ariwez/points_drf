from django.db import models

from points_drf.points.models.user import User


class PointsAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Points account of: {self.user} - balance: {self.balance}'
