import pandas as pd

def calculate_buy_order(price, capital, trading_fee):
    """매수 주문을 계산하는 함수 (수수료를 고려하여 자본 내에서 계산)"""
    buy_price = price * (1 + trading_fee)
    quantity = capital / buy_price
    capital -= buy_price * quantity
    return buy_price, quantity, capital

    # # 수수료를 제외한 실제 매수 가능 자본
    # available_capital = capital / (1 + trading_fee)
    
    # # 실제 매수 가능한 수량 계산
    # quantity = available_capital / price
    
    # # 총 매수 금액 (수수료를 제외한 금액)
    # total_cost = price * quantity
    
    # # 수수료 계산
    # fee = total_cost * trading_fee
    
    # # 자본에서 매수 금액과 수수료 차감
    # capital -= (total_cost + fee)
    
    # return price, quantity, capital


def calculate_sell_order(price, buy_price, quantity, capital, trading_fee):
    """매도 주문을 계산하고 수익률을 반환하는 함수 (수수료를 고려하여 계산)"""
    sell_price = price * (1 - trading_fee)
    capital += sell_price * quantity
    profit = (sell_price - buy_price) * quantity
    rate_of_return = (profit / (buy_price * quantity)) * 100  # 수익률 계산
    return sell_price, capital, profit, rate_of_return
    # 매도 금액에서 수수료 차감
    # total_sell_value = price * quantity
    # fee = total_sell_value * trading_fee
    # sell_price_after_fee = total_sell_value - fee  # 수수료 차감 후 매도 금액

    # # 자본에 매도 금액 추가
    # capital += sell_price_after_fee

    # # 수익 계산
    # profit = (price - buy_price) * quantity - fee  # 매도 후 수익에서 수수료 차감
    
    # # 수익률 계산 (수수료를 고려한 실질 수익률)
    # rate_of_return = (profit / (buy_price * quantity)) * 100  # 수익률(%)

    # return price, capital, profit, rate_of_return



def generic_trading_simulation(df, initial_capital, trading_fee, position_col='Positions', ma_cols=None):
    """
    SMA 또는 Golden Cross 기반 매매 전략을 시뮬레이션하는 일반화된 함수.

    Args:
        df (pd.DataFrame): 가격 데이터 및 신호가 포함된 데이터프레임
        initial_capital (float): 초기 자본
        trading_fee (float): 거래 수수료 비율
        position_col (str): 포지션 신호가 담긴 컬럼 이름
        ma_cols (list): 이동 평균 값을 나타내는 컬럼 리스트 (예: ['short_MA', 'long_MA'] 또는 ['5MA'])

    Returns:
        pd.DataFrame: 매매 기록 데이터프레임
    """
    trades = []
    in_position = False
    capital = initial_capital
    buy_price = 0

    for i in range(1, len(df)):
        close_price = df['Close'].iloc[i]
        current_time = df['Time'].iloc[i]
        position_signal = df[position_col].iloc[i]
        
        ma_values = [df[col].iloc[i] for col in ma_cols]  # 각 이동 평균 값을 가져옴

        # 매수 조건: 포지션 값이 1이고 포지션이 없는 경우
        if position_signal == 1 and not in_position:
            buy_price, quantity, capital = calculate_buy_order(close_price, capital, trading_fee)
            in_position = True
            trades.append(('buy', current_time, close_price, *ma_values, quantity, capital, None, None))

        # 매도 조건: 포지션 값이 -1이고 포지션이 있는 경우
        elif position_signal == -1 and in_position:
            sell_price, capital, profit, return_rate = calculate_sell_order(close_price, buy_price, quantity, capital, trading_fee)
            in_position = False
            trades.append(('sell', current_time, close_price, *ma_values, quantity, capital, profit, return_rate))

    # 결과를 데이터프레임으로 반환
    columns = ['Action', 'Time', 'Close'] + ma_cols + ['Quantity', 'Capital', 'Profit', 'Return Rate (%)']
    trades_df = pd.DataFrame(trades, columns=columns)
    trades_df = trades_df.fillna('')  # NaN 값을 빈 문자열로 대체
    return trades_df
