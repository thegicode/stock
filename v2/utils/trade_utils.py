def calculate_buy_order(price, capital, trading_fee):
    """매수 주문을 계산하는 함수 (수수료를 고려하여 자본 내에서 계산)"""
    # 수수료를 제외한 실제 매수 가능 자본
    available_capital = capital / (1 + trading_fee)
    
    # 실제 매수 가능한 수량 계산
    quantity = available_capital / price
    
    # 총 매수 금액 (수수료를 제외한 금액)
    total_cost = price * quantity
    
    # 수수료 계산
    fee = total_cost * trading_fee
    
    # 자본에서 매수 금액과 수수료 차감
    capital -= (total_cost + fee)
    
    return price, quantity, capital


def calculate_sell_order(price, buy_price, quantity, capital, trading_fee):
    """매도 주문을 계산하고 수익률을 반환하는 함수 (수수료를 고려하여 계산)"""
    # 매도 금액에서 수수료 차감
    total_sell_value = price * quantity
    fee = total_sell_value * trading_fee
    sell_price_after_fee = total_sell_value - fee  # 수수료 차감 후 매도 금액

    # 자본에 매도 금액 추가
    capital += sell_price_after_fee

    # 수익 계산
    profit = (price - buy_price) * quantity - fee  # 매도 후 수익에서 수수료 차감
    
    # 수익률 계산 (수수료를 고려한 실질 수익률)
    rate_of_return = (profit / (buy_price * quantity)) * 100  # 수익률(%)

    return price, capital, profit, rate_of_return
