from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from points_drf.api.serializers.balance import BalanceSerializer
from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_source import PointsSource
from points_drf.points.services import PointsService


class PointsAccountDetail(APIView):
    """Detail view for points account with balance update form"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account_detail.html'
    permission_classes = [AllowAny]

    def get(self, request, pk):
        points_account: PointsAccount = get_object_or_404(PointsAccount, pk=pk)
        serializer: BalanceSerializer = BalanceSerializer()
        return Response({'serializer': serializer, 'points_account': points_account})

    def post(self, request, pk):
        points_account: PointsAccount = get_object_or_404(PointsAccount, pk=pk)
        serializer: BalanceSerializer = BalanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'serializer': serializer,
                    'points_account': points_account
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        amount: int = serializer.validated_data['amount']
        source: PointsSource = PointsSource.objects.get(key=serializer.validated_data['source_key'])

        if serializer.validated_data['remove_points']:
            PointsService().remove(points_account.user, source, amount)
        else:
            PointsService().add(points_account.user, source, amount)

        return redirect('points_account_detail_view', pk=pk)
