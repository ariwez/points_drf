from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from points_drf.points.models.points_account import PointsAccount
from points_drf.points.tests.factories import AccountModelFactory


class PointsAccountListViewTest(APITestCase):

    def test_empty_list_points_account(self) -> None:
        url: str = reverse('points_account_list_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_populated_list_points_account(self) -> None:
        first_user_account: PointsAccount = AccountModelFactory(balance=100)
        last_user_account: PointsAccount = AccountModelFactory(balance=200)

        url: str = reverse('points_account_list_view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'],
                         [
                             {
                                 'user': {
                                     'id': first_user_account.user.id,
                                     'first_name': first_user_account.user.first_name,
                                     'last_name': first_user_account.user.last_name,
                                     'email': first_user_account.user.email,
                                     'referrer_email': first_user_account.user.referrer_email,
                                 },
                                 'balance': first_user_account.balance,
                             },
                             {
                                 'user': {
                                     'id': last_user_account.user.id,
                                     'first_name': last_user_account.user.first_name,
                                     'last_name': last_user_account.user.last_name,
                                     'email': last_user_account.user.email,
                                     'referrer_email': last_user_account.user.referrer_email,
                                 },
                                 'balance': last_user_account.balance,
                             },
                         ]
                         )
