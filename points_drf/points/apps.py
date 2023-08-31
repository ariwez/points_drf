from django.apps import AppConfig


class PointsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'points_drf.points'

    def ready(self):
        import points_drf.points.receivers
