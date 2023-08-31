from django.db import models


class PointsSource(models.Model):
    key = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)
    value = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f' {self.key} value: {self.value}'
