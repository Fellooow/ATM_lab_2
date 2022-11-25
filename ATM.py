from View import *


class User:
    pass


class Card:
    def __init__(self, account=None, expiration_date=None):
        self.__account = account
        self.__expiration_date = expiration_date


class Banknote:
    def __init__(self, denomination=None, currency=None):
        self.__denomination = denomination
        self.__currency = currency


class MoneyVault:
    def __init__(self, banknote_amount=None):
        self._banknote_amount: dict = banknote_amount

    def getMoney(self, amount:int) -> None:
        #Взять деньги из хранилища

class ATM:
    def __init__(self, account_pin=None):
        self.__account_pin: list = account_pin