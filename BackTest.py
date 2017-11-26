from TradingDay import TradingDay
import random
import pandas as pd


class BackTest:
    @staticmethod
    def get_random_signal(code_list, start_date, end_date, size):
        trading_day_list = TradingDay.get_trading_day_list(start_date, end_date)
        signal = pd.DataFrame(columns=('code', 'date'))
        for _ in range(size):
            signal.loc[len(signal)] = [random.choice(code_list), random.choice(trading_day_list)]
        signal['date'] = signal['date'].astype('int')
        return signal
