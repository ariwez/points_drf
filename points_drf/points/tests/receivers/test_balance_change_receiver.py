import unittest

from django.test import TestCase


class ReceiversTest(TestCase):

    @unittest.skip("Test should mock method called inside handler (e.g. send_email), currently not implemented")
    def test_handler_is_called_after_save(self) -> None:
        pass
