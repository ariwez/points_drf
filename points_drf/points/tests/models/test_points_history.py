from django.test import TestCase

from points_drf.points.models.points_history import PointsHistory
from points_drf.points.tests.factories import AccountModelFactory, SourceModelFactory


class PointsHistoryTest(TestCase):

    def test_create(self) -> None:
        parameters: dict = {
            'account': AccountModelFactory(),
            'source': SourceModelFactory(),
            'value': 100,
            'balance': 100,
        }
        points_history: PointsHistory = PointsHistory.objects.create(**parameters)

        self.assertEqual(points_history.account, parameters['account'])
        self.assertEqual(points_history.source, parameters['source'])
        self.assertEqual(points_history.value, parameters['value'])
        self.assertEqual(points_history.balance, parameters['balance'])
        self.assertIsNotNone(points_history.created_at)
        self.assertIsNotNone(points_history.updated_at)
