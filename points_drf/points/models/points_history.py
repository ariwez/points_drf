from django.db import models

from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_source import PointsSource


class PointsHistory(models.Model):
    account = models.ForeignKey(PointsAccount, on_delete=models.CASCADE)
    source = models.ForeignKey(PointsSource, on_delete=models.SET_NULL, null=True)
    value = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.source.key}] {self.account.user.email} change {self.value} at: {self.created_at}'
