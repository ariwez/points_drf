import logging
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import (
    IntegrityError,
    transaction,
)
from django.db.models import F

from .errors import InvalidAmountError
from .models.points_account import PointsAccount
from .models.points_source import PointsSource
from .models.points_history import PointsHistory
from .models.user import User

logger = logging.getLogger()


class PointsService:
    def create_account_for_user(
            self,
            first_name: str,
            last_name: str,
            email: str,
            referrer_email: str,
            balance: int
    ) -> Optional[PointsAccount]:
        """Create a new user account with a given balance of points"""
        try:
            with transaction.atomic():
                user: User = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    referrer_email=referrer_email
                )
                return PointsAccount.objects.create(user=user, balance=balance)
        except (IntegrityError, ValueError, ValidationError) as error:
            logger.error(f"Error creating user account: {email} - {error}")

    def add(
            self,
            user: User,
            source: PointsSource,
            amount: Optional[int] = None,
    ) -> int:
        """Add points to a user's account"""
        amount: int = amount or source.value
        if amount <= 0:
            raise InvalidAmountError(amount)

        try:
            self._update_balance(user, source, amount)
        except IntegrityError as error:
            logger.error(f"Error adding points: {user.email} - {error}")
            return 0

        return amount

    def remove(
            self,
            user: User,
            source: PointsSource,
            amount: Optional[int] = None,
    ) -> int:
        """Remove points from a user's account"""
        amount: int = amount or source.value
        if amount <= 0:
            raise InvalidAmountError(amount)

        try:
            self._update_balance(user, source, -amount)
        except IntegrityError as error:
            logger.error(f"Error removing points: {user.email} - {error}")
            return 0

        return amount

    def _update_balance(self, user: User, source: PointsSource, amount: int):
        """
        Update a user's points balance, create a history record
        raises ObjectDoesNotExist if the account does not exist
        """
        with transaction.atomic():
            points_account = PointsAccount.objects.select_for_update().get(user=user)
            points_account.balance = F('balance') + amount
            points_account.save()
            points_account.refresh_from_db()
            PointsHistory.objects.create(
                account=points_account,
                source=source,
                value=amount,
                balance=points_account.balance
            )
