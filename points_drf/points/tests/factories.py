import factory

from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_source import PointsSource
from points_drf.points.models.user import User


class UserModelFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    class Meta:
        model = User


class AccountModelFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory('points_drf.points.tests.factories.UserModelFactory')

    class Meta:
        model = PointsAccount


class SourceModelFactory(factory.django.DjangoModelFactory):
    key = factory.Faker('name')
    description = factory.Faker('sentence')

    class Meta:
        model = PointsSource
