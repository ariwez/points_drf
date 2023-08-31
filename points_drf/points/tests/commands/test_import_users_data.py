import logging
from io import StringIO
from unittest import mock

import pandas as pd
from django.core.management import call_command
from django.test import TestCase

from points_drf.points import settings
from points_drf.points.management.commands.import_users_data import Command
from points_drf.points.models.points_account import PointsAccount
from points_drf.points.models.points_history import PointsHistory
from points_drf.points.models.user import User
from points_drf.points.tests.factories import AccountModelFactory, UserModelFactory

logger = logging.getLogger()


class ImportUsersDataTest(TestCase):

    def call_command(self, *args, **kwargs) -> str:
        out = StringIO()
        call_command(
            "import_users_data",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    def test_user_import_with_data(self) -> None:
        user_data: dict = {
            "id": [1, 2, 3,],
            "first_name": ["John", "Jane", "Joe"],
            "last_name": ["Doe", "Smith", "Walker"],
            "email": ["t@x.com", "js@z.com", "jw@y.com"],
            "referrer_email": ["", "", "js@z.com"],
            "balance": [100, 200, 300],
        }
        csv: str = pd.DataFrame(data=user_data).to_csv()

        with self.assertLogs(logger=logger, level='INFO') as logs:
            with mock.patch(
                    "points_drf.points.management.commands.import_users_data.Command.read_csv",
                    return_value=pd.read_csv(StringIO(csv), chunksize=1, iterator=True)
            ) as mock_read_csv:
                out: str = self.call_command("example.csv")
                self.assertIn("INFO:root:Importing users data from example.csv", logs.output)
                self.assertIn("INFO:root:Import finished: 3 users imported", logs.output)
                self.assertEqual(User.objects.count(), 3)
                self.assertEqual(PointsAccount.objects.count(), 3)
                self.assertEqual(PointsHistory.objects.count(), 1)
                self.assertEqual(PointsAccount.objects.get(user__email="t@x.com").balance, 100)
                self.assertEqual(PointsAccount.objects.get(user__email="js@z.com").balance, 200 + 20)
                self.assertEqual(PointsHistory.objects.get(
                    account__user__email="js@z.com").source.key,
                    settings.REFFERAL_BONUS_KEY
                )
                self.assertEqual(PointsAccount.objects.get(user__email="jw@y.com").balance, 300)

    def test_command_run_with_missing_file_fails(self) -> None:
        with self.assertLogs(logger=logger, level='ERROR') as logs:
            out: str = self.call_command("invalid.csv")
            self.assertIn(
                "ERROR:root:Error importing users data: [Errno 2] No such file or directory: 'invalid.csv'",
                logs.output
            )

    def test_command_run_with_existing_user_logs_error(self) -> None:
        email: str = "jd@example.com"
        user: User = UserModelFactory(email=email)
        user_data: dict = {
            "id": 1,
            "first_name": [user.first_name],
            "last_name": [user.last_name],
            "email": [user.email],
            "referrer_email": [''],
            "balance": [100],
        }
        with self.assertLogs(logger=logger, level='ERROR') as logs:
            with mock.patch(
                    "points_drf.points.management.commands.import_users_data.Command.read_csv",
                    return_value=[pd.DataFrame(data=user_data)],
            ) as mock_read_csv:
                out: str = self.call_command("example.csv")
                self.assertIn(
                    "ERROR:root:Error creating user account: jd@example.com - {'email': ['User with this Email already exists.']}",
                    logs.output
                )

    def test_referral_bonus_for_existing_users(self) -> None:
        first_referrer_account: PointsAccount = AccountModelFactory(balance=10)
        last_referrer_account: PointsAccount = AccountModelFactory(balance=30)

        self.assertEqual(first_referrer_account.balance, 10)
        self.assertEqual(last_referrer_account.balance, 30)

        referrers_emails: list[str] = [
            first_referrer_account.user.email,
            last_referrer_account.user.email,
        ]

        Command().grant_referral_bonuses(referrers_emails)

        first_referrer_account.refresh_from_db()
        self.assertEqual(first_referrer_account.balance, 30)
        points_history = PointsHistory.objects.filter(account=first_referrer_account).first()
        self.assertEqual(points_history.source.key, 'referral_bonus')
        last_referrer_account.refresh_from_db()
        self.assertEqual(last_referrer_account.balance, 50)
        points_history = PointsHistory.objects.filter(account=last_referrer_account).first()
        self.assertEqual(points_history.source.key, 'referral_bonus')

    def test_referral_bonus_for_missing_users(self) -> None:
        missing_user_email: str = 'jack@example.com'
        referrers_emails: list[str] = [missing_user_email]
        with self.assertLogs(logger=logger, level='ERROR') as logs:
            Command().grant_referral_bonuses(referrers_emails)
            self.assertIn(
                f"ERROR:root:User with email {missing_user_email} does not exist, cannot add referral bonus",
                logs.output
            )
