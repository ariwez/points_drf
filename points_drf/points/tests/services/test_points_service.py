from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from points_drf.points.errors import InvalidAmountError
from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_history import PointsHistory
from points_drf.points.models.points_source import PointsSource
from points_drf.points.models.user import User
from points_drf.points.services import PointsService
from points_drf.points.tests.factories import AccountModelFactory, SourceModelFactory, UserModelFactory


class PointsServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user: User = UserModelFactory()
        self.source: PointsSource = SourceModelFactory(value=100)
        self.points_service: PointsService = PointsService()
        self.points_account: PointsAccount = AccountModelFactory(user=self.user)

    def test_create_account_for_user(self) -> None:
        params: dict = {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'js@example.com',
            'referrer_email': '',
            'balance': 100,
        }

        self.assertIsNone(User.objects.filter(email=params['email']).first())
        self.assertIsNone(PointsAccount.objects.filter(user__email=params['email']).first())

        self.points_service.create_account_for_user(**params)

        user: User = User.objects.get(email=params['email'])
        self.assertEqual(user.first_name, params['first_name'])
        self.assertEqual(user.last_name, params['last_name'])
        self.assertEqual(user.email, params['email'])
        self.assertEqual(user.referrer_email, params['referrer_email'])
        points_account: PointsAccount = PointsAccount.objects.get(user=user)
        self.assertEqual(points_account.balance, params['balance'])

    def test_add_points_from_source(self) -> None:
        value: int = 100
        result: int = self.points_service.add(self.user, self.source)

        self.assertEqual(result, value)
        points_account = PointsAccount.objects.get(user=self.user)
        self.assertEqual(points_account.balance, value)
        points_history = PointsHistory.objects.get(account=points_account)
        self.assertEqual(points_history.value, value)
        self.assertEqual(points_history.balance, value)
        self.assertEqual(points_history.source, self.source)

    def test_add_points_from_source_with_amount(self) -> None:
        amount: int = 500
        result: int = self.points_service.add(self.user, self.source, amount)

        self.assertEqual(result, amount)
        points_account = PointsAccount.objects.get(user=self.user)
        self.assertEqual(points_account.balance, amount)
        points_history = PointsHistory.objects.get(account=points_account)
        self.assertEqual(points_history.value, amount)
        self.assertEqual(points_history.balance, amount)
        self.assertEqual(points_history.source, self.source)

    def test_add_points_with_invalid_amount_raises_error(self) -> None:
        source: PointsSource = SourceModelFactory(value=100)
        with self.assertRaisesMessage(InvalidAmountError, 'Invalid amount: -100'):
            self.points_service.add(self.user, source, -100)

    def test_remove_points_from_source(self) -> None:
        value: int = 100
        result: int = self.points_service.remove(self.user, self.source)

        self.assertEqual(result, value)
        points_account = PointsAccount.objects.get(user=self.user)
        self.assertEqual(points_account.balance, -value)
        points_history = PointsHistory.objects.get(account=points_account)
        self.assertEqual(points_history.value, -value)
        self.assertEqual(points_history.balance, -value)
        self.assertEqual(points_history.source, self.source)

    def test_remove_points_from_source_with_amount(self) -> None:
        amount: int = 500
        result: int = self.points_service.remove(self.user, self.source, amount)

        self.assertEqual(result, amount)
        points_account = PointsAccount.objects.get(user=self.user)
        self.assertEqual(points_account.balance, -amount)
        points_history = PointsHistory.objects.get(account=points_account)
        self.assertEqual(points_history.value, -amount)
        self.assertEqual(points_history.balance, -amount)
        self.assertEqual(points_history.source, self.source)

    def test_remove_points_with_invalid_amount_raises_error(self) -> None:
        source: PointsSource = SourceModelFactory(value=100)
        with self.assertRaisesMessage(InvalidAmountError, 'Invalid amount: -100'):
            self.points_service.remove(self.user, source, -100)

    def test_add_without_account_raises_error(self) -> None:
        user: User = UserModelFactory()
        with self.assertRaisesMessage(ObjectDoesNotExist, 'PointsAccount matching query does not exist.'):
            self.points_service.add(user, self.source)

    def test_remove_without_account_raises_error(self) -> None:
        user: User = UserModelFactory()
        with self.assertRaisesMessage(ObjectDoesNotExist, 'PointsAccount matching query does not exist.'):
            self.points_service.remove(user, self.source)
