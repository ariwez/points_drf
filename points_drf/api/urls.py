from django.urls import path
from rest_framework.routers import DefaultRouter

from points_drf.api.views.points.detail import PointsAccountDetail
from points_drf.api.views.points.list import PointsAccountListView

router = DefaultRouter()

urlpatterns = router.urls + [
    path('points/', PointsAccountListView.as_view(), name="points_account_list_view"),
    path('points/<int:pk>', PointsAccountDetail.as_view(), name="points_account_detail_view"),
]
