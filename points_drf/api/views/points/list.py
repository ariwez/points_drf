from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer

from points_drf.api.serializers.points_account import PointsAccountSerializer
from points_drf.points.models.points_account import PointsAccount


class PointsAccountListView(ListAPIView):
    """List view for points accounts"""
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    queryset = PointsAccount.objects.all().order_by('created_at')
    template_name = 'accounts_list.html'
    serializer_class = PointsAccountSerializer
