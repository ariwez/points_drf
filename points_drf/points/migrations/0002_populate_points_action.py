from django.db import migrations

from points_drf.points import settings
from points_drf.points.models.points_source import PointsSource


def populate_points_sources(apps, schema_editor):
    """Populate points sources."""
    PointsSource.objects.get_or_create(
        key=settings.REFFERAL_BONUS_KEY,
        description='Bonus points for creating a new account by referral',
        value=settings.REFFERAL_BONUS_VALUE,
    )

    PointsSource.objects.get_or_create(
        key=settings.ADMIN_ADD_POINTS_KEY,
        description='Admin add points, amount must be specified explicitly',
    )

    PointsSource.objects.get_or_create(
        key=settings.ADMIN_REMOVE_POINTS_KEY,
        description='Admin remove points, amount must be specified explicitly',
    )


class Migration(migrations.Migration):
    dependencies = [
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_points_sources,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
