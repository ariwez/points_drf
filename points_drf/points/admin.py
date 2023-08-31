from django.contrib import admin

from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_source import PointsSource
from points_drf.points.models.points_history import PointsHistory
from points_drf.points.models.user import User

admin.site.register(User)
admin.site.register(PointsAccount)
admin.site.register(PointsHistory)
admin.site.register(PointsSource)
