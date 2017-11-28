import sys
import datetime


CLOSE_DAY_FILE = r'close_day.txt'


def get_close_date_list():
    # 휴장일을 텍스트파일로부터 받아옴
    # 양식 : YYYYMMDD
    # 20140101
    # 20140505
    # 20140815
    try:
        with open(CLOSE_DAY_FILE, 'r') as f:
            close_date_list = []
            for line in f.readlines():
                date = line.split("\n")[0]
                close_date_list.append(date)
    except FileNotFoundError:
        print('휴장일 데이터 파일이 없음')
        sys.exit(-1)
    return tuple(close_date_list)


def get_trading_days_list(min_year=2010, size=4000):
    # 임의로 2010년 부터 시작함
    base = datetime.date(min_year, 1, 1)
    date_list = [base + datetime.timedelta(days=x) for x in range(0, size)]

    # 주말제외한 리스트
    week_days_list = []
    for date in date_list:
        if date.weekday() not in [5, 6]:  # 5:토요일 6:일요일
            week_days_list.append(date)

    # 휴장일 제외
    close_date_list = get_close_date_list()
    close_date_time_list = []
    for close_date in close_date_list:
        close_date_time_list.append(datetime.datetime.strptime(close_date, '%Y%m%d').date())
    trading_days_list = list(set(week_days_list) - set(close_date_time_list))
    trading_days_list.sort()
    return tuple(trading_days_list)


class TradingDay:
    trading_days_list = get_trading_days_list()

    def __init__(self, target):
        self.target_date = datetime.datetime.strptime(str(target), '%Y%m%d').date()
        if self.target_date not in TradingDay.trading_days_list:
            raise ValueError(target, '는 휴장일')

    def get_target_date(self):
        return self.target_date

    def get_target_date_str_t(self):
        return self.target_date.strftime('%Y%m%d')

    def get_target_date_int_t(self):
        return int(self.get_target_date_str_t())

    def set_target_date(self, target):
        temp_date = datetime.datetime.strptime(str(target), '%Y%m%d').date()
        if temp_date not in self.trading_days_list:
            raise IndexError(temp_date, '는 휴장일')
        else:
            self.target_date = temp_date

    def delta(self, days):
        index = TradingDay.trading_days_list.index(self.get_target_date())
        return TradingDay.trading_days_list[index + days]

    def delta_str_t(self, days):
        return self.delta(days).strftime('%Y%m%d')

    def delta_int_t(self, days):
        return int(self.delta_str_t(days))

    @staticmethod
    def trading_days_between_date(cur_date, target_date):
        """
        cur_date, target_date : int 타입
        cur_date 가 target_date 로 부터 몇 거래일인지 리턴해줌
        :return:
        """
        cur_date = datetime.datetime.strptime(str(cur_date), '%Y%m%d').date()
        target_date = datetime.datetime.strptime(str(target_date), '%Y%m%d').date()
        cur_date_index = TradingDay.trading_days_list.index(cur_date)
        target_date_index = TradingDay.trading_days_list.index(target_date)
        return cur_date_index - target_date_index

    @staticmethod
    def get_trading_day_list(start_date, end_date):
        start_date = datetime.datetime.strptime(str(start_date), '%Y%m%d').date()
        end_date = datetime.datetime.strptime(str(end_date), '%Y%m%d').date()

        if start_date not in TradingDay.trading_days_list:
            raise ValueError(start_date, '휴장일')
        elif end_date not in TradingDay.trading_days_list:
            raise ValueError(end_date, '휴장일')

        std_idx = TradingDay.trading_days_list.index(start_date)
        end_idx = TradingDay.trading_days_list.index(end_date)
        return [int(date.strftime('%Y%m%d')) for date in TradingDay.trading_days_list[std_idx:end_idx + 1]]

    @staticmethod
    def trading_days_by_year(year):
        date_list = []
        for date in TradingDay.trading_days_list:
            if date.year == year:
                date_list.append(int(date.strftime('%Y%m%d')))
        return date_list

    @staticmethod
    def trading_days_by_year_n_month(year, month):
        """
        year, month 인자로 받아
        거래일 리스트 리턴
        """
        date_list = []
        for date in TradingDay.trading_days_list:
            if date.year == year and date.month == month:
                date_list.append(int(date.strftime('%Y%m%d')))
        return date_list

    @staticmethod
    def expiration_date(year, month):
        """
        만기일은 매달 두번째 목요일
        연도와 달을 인자로 받아
        만기일을 리턴하는 함수
        """
        first_thursday = None
        for i in range(1, 8):
            date = datetime.datetime(year, month, i).date()
            if date.weekday() == 3:
                first_thursday = date
        second_thursday = int((first_thursday + datetime.timedelta(days=7)).strftime('%Y%m%d'))

        trading_days = TradingDay.trading_days_by_year_n_month(year, month)
        if second_thursday in trading_days:
            return second_thursday
        else:
            trading_days.reverse()
            for date in trading_days:
                if date < second_thursday:
                    return date

    @staticmethod
    def magnet(date, flag):
        """
        flag:: before:0, after:1
        """
        date = datetime.datetime.strptime(str(date), '%Y%m%d').date()
        idx = 0
        for trading_day in TradingDay.trading_days_list:
            if date <= trading_day:
                break
            idx += 1
        if date == TradingDay.trading_days_list[idx]:
            return TradingDay.trading_days_list[idx]
        else:
            if flag == 0:
                return TradingDay.trading_days_list[idx-1]
            else:
                return TradingDay.trading_days_list[idx]
