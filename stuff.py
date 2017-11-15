def get_ratio(standard_price, present_price):
    result = (present_price - standard_price)/standard_price
    return result * 100
    
def price_for_bid_ask(price, close2up=True):
    """
    실수로 표현된 가격을 호가가격단위로 변화해줌
    :return: 호가가격
    """
    if price < 1000:
        bid = 1
    elif 1000 <= price < 5000:
        bid = 5
    elif 5000 <= price < 10000:
        bid = 10
    elif 10000 <= price < 50000:
        bid = 50
    elif 50000 <= price < 100000:
        bid = 100
    elif 100000 <= price < 500000:
        bid = 500
    elif price >= 500000:
        bid = 1000
    else:
        raise ValueError
    quo = price // bid
    remain = price % bid
    if remain == 0:
        return quo * bid
    else:
        if close2up:
            return quo * bid + bid
        else:
            return quo * bid
