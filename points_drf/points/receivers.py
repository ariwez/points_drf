from django.db.models.signals import post_save
from django.dispatch import receiver

from points_drf.points.models.points_account import PointsAccount


@receiver(post_save, sender=PointsAccount)
def on_balance_change(sender, created, **kwargs):
    # Empty function for handling balance change, email sending, etc.
    pass
