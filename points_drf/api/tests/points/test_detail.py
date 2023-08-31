from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_source import PointsSource
from points_drf.points.tests.factories import AccountModelFactory, SourceModelFactory


class PointsAccountDetailsTest(APITestCase):

    def setUp(self) -> None:
        self.points_account: PointsAccount = AccountModelFactory(balance=100)
        self.points_source: PointsSource = SourceModelFactory()
        self.url: str = reverse('points_account_detail_view', kwargs={'pk': self.points_account.pk})

    def test_detail_point_account(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['points_account'], self.points_account)

    def test_detail_point_not_found(self) -> None:
        invalid_pk: int = 999
        url: str = reverse('points_account_detail_view', kwargs={'pk': invalid_pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data['detail']), 'Not found.')

    def test_balance_change_without_data(self) -> None:
        response = self.client.post(self.url, data={})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['serializer'].errors,
            {
                'amount': ['This field is required.'],
                'source_key': ['This field is required.']
            }
        )

    def test_balance_add_points(self) -> None:
        response = self.client.post(self.url, data={'amount': 100, 'source_key': self.points_source.key})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.points_account.refresh_from_db()
        self.assertEqual(self.points_account.balance, 200)

    def test_balance_remove_points(self) -> None:
        response = self.client.post(
            self.url,
            data={
                'amount': 50,
                'source_key': self.points_source.key,
                'remove_points': True
            }
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.points_account.refresh_from_db()
        self.assertEqual(self.points_account.balance, 50)

    def test_balance_change_with_invalid_amount(self) -> None:
        invalid_amount: int = -100
        response = self.client.post(self.url, data={'amount': invalid_amount, 'source_key': self.points_source.key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['serializer'].errors), 1)
        self.assertEqual(response.data['serializer'].errors['amount'][0].code, 'min_value')

    def test_balance_change_with_invalid_source(self) -> None:
        invalid_source_key: str = 'invalid-source-key'
        response = self.client.post(self.url, data={'amount': 100, 'source_key': invalid_source_key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['serializer'].errors['source_key'][0]),
            'Points source with key: invalid-source-key does not exist.'
        )

    def test_balance_change_with_account_not_found(self) -> None:
        invalid_pk: int = 999
        url: str = reverse('points_account_detail_view', kwargs={'pk': invalid_pk})
        response = self.client.post(url, data={'amount': 100, 'source_key': self.points_source.key})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(str(response.data['detail']), 'Not found.')
