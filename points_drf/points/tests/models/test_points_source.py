from django.test import TestCase

from points_drf.points.models.points_source import PointsSource


class PointsSourceTest(TestCase):

    def test_create(self) -> None:
        parameters: dict = {
            'key': 'bonus_points_source',
            'description': 'Bonus points source',
            'value': 100,
        }
        points_source: PointsSource = PointsSource.objects.create(**parameters)

        self.assertEqual(points_source.key, parameters['key'])
        self.assertEqual(points_source.description, parameters['description'])
        self.assertEqual(points_source.value, parameters['value'])
        self.assertIsNotNone(points_source.created_at)
        self.assertIsNotNone(points_source.updated_at)
