class Error(Exception):
    pass


class InvalidAmountError(Error):
    def __init__(self, amount: int):
        self.amount: int = amount

    def __str__(self) -> str:
        return f'Invalid amount: {self.amount}'
