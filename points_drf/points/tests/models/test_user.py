from django.core.exceptions import ValidationError
from django.test import TestCase

from points_drf.points.models.user import User
from points_drf.points.tests.factories import UserModelFactory


class UserTest(TestCase):

    def test_create(self) -> None:
        parameters: dict = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'js@example.com',
            'referrer_email': '',
        }
        user: User = User.objects.create(**parameters)

        self.assertEqual(user.first_name, parameters['first_name'])
        self.assertEqual(user.last_name, parameters['last_name'])
        self.assertEqual(user.email, parameters['email'])
        self.assertEqual(user.referrer_email, parameters['referrer_email'])
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_create_with_invalid_email_raises_error(self) -> None:
        parameters: dict = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'referrer_email': '',
        }
        with self.assertRaisesMessage(ValidationError, 'Enter a valid email address.'):
            User.objects.create(**parameters)

    def test_create_with_existing_email_raises_error(self) -> None:
        email: str = 'test-email@example.com'
        user: User = UserModelFactory(email=email)

        parameters: dict = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': email,
        }

        with self.assertRaisesMessage(ValidationError, 'User with this Email already exists.'):
            User.objects.create(**parameters)

    def test_create_with_invalid_referrer_email_raises_error(self) -> None:
        parameters: dict = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test-email@example.com',
            'referrer_email': 'invalid-referrer-email',
        }
        with self.assertRaisesMessage(ValidationError, 'Enter a valid email address.'):
            User.objects.create(**parameters)

    def test_create_without_first_name_raises_error(self) -> None:
        parameters: dict = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'test-email@example.com',
        }

        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            User.objects.create(**parameters)

    def test_create_without_last_name_raises_error(self) -> None:
        parameters: dict = {
            'first_name': 'John',
            'last_name': '',
            'email': 'test-email@example.com'
        }

        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            User.objects.create(**parameters)

    def test_create_without_email_raises_error(self) -> None:
        parameters: dict = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '',
        }
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            User.objects.create(**parameters)
