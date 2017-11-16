import numpy as np
import pandas as pd
import TradingDay


class IndexBASE(metaclass=ABCMeta):
    def __init__(self, code_list, weight_list, base_date):
        """
        :param code_list: 지수의 구성 종목리스트
        ex) ['A005930', 'A000660', ...]
        :param weight_list: 구성종목의 비중리스트
        ex) [0.2, 0.3, ...] (합 1)
        :param base_date: 지수설정 기준일
        ex) 20170104
        """
        self.base_date = TradingDay(base_date)
        self.code_list = code_list
        self.weight_list = weight_list
        if len(self.code_list) != len(self.weight_list):
            # 코드리스트와 비중리스트의 개수가 다른 경우
            raise ValueError
        total = 0
        for weight in self.weight_list:
            total += weight
        if total > 1.001:
            # 1이여도 1.000000000000000002 나옴...
            raise ValueError('%d' % total)

        # 가격 데이터를 저장할 DataFrame
        self.price_table = pd.DataFrame(columns=('code', ))
        self.price_table.set_index('code', inplace=True)
        self.price_table.index.name = None
        # 수익률을 저장할 DataFrame
        self.performance_table = pd.DataFrame(columns=('code', ))
        self.performance_table.set_index('code', inplace=True)
        self.performance_table.index.name = None

    def run(self, delta):
        """
        :param delta: 기간
         ex) 10
        """
        start_date = self.base_date.get_target_date_int_t()
        end_date = self.base_date.delta_int_t(delta)

        # delta 크기만큼 컬럼 추가
        for days in range(0, delta+1):
            self.price_table['D+%d' % days] = None

        for code in self.code_list:
            data = Index.get_adjusted_price(code, start_date, end_date)
            if data.shape[0] != delta+1:
                # 데이터가 부족
                raise ValueError('%s' % code)
            self.price_table.loc[code, :] = data.values
            self.performance_table.loc[code, 'D+0'] = 0

        for i in range(delta+1):
            if i == 0:
                continue
            ratio = self.price_table.loc[:, ['D+0', 'D+%d' % i]].apply(IndexBASE.get_ratio_for_data_frame, 1)
            self.performance_table.loc[:, 'D+%d' % i] = ratio

    @staticmethod
    @abstractmethod
    def get_adjusted_price(code, start_date, end_date):
        """
        :return: 종가 Series
        """
        pass

    @staticmethod
    def get_ratio_for_data_frame(col):
        standard_price, present_price = col[0], col[1]
        try:
            result = (present_price - standard_price) / standard_price
        except Exception:
            return np.NaN
        return result * 100
