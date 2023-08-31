import logging
from typing import Optional, Iterator

import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import signals

from points_drf.points import settings
from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_source import PointsSource
from points_drf.points.models.user import User
from points_drf.points.receivers import on_balance_change
from points_drf.points.services import PointsService

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Imports users data from a CSV file, post_save signal is disconnected to avoid i.e. sending emails"
    CHUNK_SIZE = 1
    points_service = PointsService()

    def add_arguments(self, parser) -> None:
        parser.add_argument("filename", type=str)

    def grant_referral_bonuses(self, referrers_emails: list[str]) -> None:
        """Grant referral bonuses to referrers"""
        referral_bonus: PointsSource = PointsSource.objects.get(key=settings.REFFERAL_BONUS_KEY)
        for email in referrers_emails:
            user: Optional[User] = User.objects.filter(email=email).first()
            if not user:
                logger.error(f"User with email {email} does not exist, cannot add referral bonus")
            else:
                self.points_service.add(
                    user=user,
                    source=referral_bonus,
                )

    def read_csv(self, filename: str) -> Iterator:
        """Reads CSV file in chunks for memory efficiency"""
        return pd.read_csv(filename, chunksize=self.CHUNK_SIZE, iterator=True)

    def handle(self, *args, **options) -> None:
        logger.info(f"Importing users data from {options['filename']}")
        users_imported: int = 0
        signals.post_save.disconnect(on_balance_change, sender=PointsAccount)

        try:
            referrers_emails_to_bonus: list[str] = []
            for row in self.read_csv(options['filename']):
                referrer_email: str = ''
                if not row['referrer_email'].isnull().values.any():
                    referrer_email = row['referrer_email'].item()

                account: Optional[PointsAccount] = self.points_service.create_account_for_user(
                    first_name=row['first_name'].item(),
                    last_name=row['last_name'].item(),
                    email=row['email'].item(),
                    referrer_email=referrer_email,
                    balance=row['balance'].item(),
                )

                if account:
                    users_imported += 1
                    if referrer_email:
                        referrers_emails_to_bonus.append(referrer_email)

            if referrers_emails_to_bonus:
                self.grant_referral_bonuses(referrers_emails_to_bonus)
        except Exception as error:
            logger.error(f"Error importing users data: {error}")

        signals.post_save.connect(on_balance_change, sender=PointsAccount)
        logger.info(f"Import finished: {users_imported} users imported")
