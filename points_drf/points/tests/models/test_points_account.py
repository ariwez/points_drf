from django.test import TestCase

from points_drf.points.models.points_account import PointsAccount
from points_drf.points.tests.factories import UserModelFactory


class PointsAccountTest(TestCase):

    def test_create(self) -> None:
        parameters: dict = {
            'user': UserModelFactory(),
            'balance': 100,
        }
        points_account: PointsAccount = PointsAccount.objects.create(**parameters)

        self.assertEqual(points_account.user, parameters['user'])
        self.assertEqual(points_account.balance, parameters['balance'])
        self.assertIsNotNone(points_account.created_at)
        self.assertIsNotNone(points_account.updated_at)
