from abc import *


class PortfolioBASE(metaclass=ABCMeta):
    """
    SEED_MONEY : 초기자본
    TAX_RATE : 세금
    COMMISSION_RATE : 수수료
    """
    SEED_MONEY = 1000 * 1000 * 1000
    TAX_RATE = 0.3 / 100
    COMMISSION_RATE = 0.015 / 100
    
    @abstractmethod
    def buy(self, code, price, amount, date):
        pass

    @abstractmethod
    def sell(self, code, price, amount):
        pass

    @abstractmethod
    def get_cash(self):
        pass

    @abstractmethod
    def get_account(self):
        pass

    @abstractmethod
    def valuation(self):
        pass

    @staticmethod
    @abstractmethod
    def cur_price(code, date):
        # for valuation method
        pass
