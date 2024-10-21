import sys
import os
import pandas as pd

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)

from v2.utils.file_utils import load_data, save_performance_to_file, save_trades_to_file
from v2.config.constants import TICKERS
from v2.utils.performance_utils import calculate_performance, format_backtest_results
from v2.utils.finantial_utils import calculate_short_long_moving_averages, signal_positions_golden_corss
from v2.utils.time_utils import extract_periods
from v2.utils.trade_utils import calculate_buy_order, calculate_sell_order



def golden_cross_trading_simulation(df, initial_capital, short_window, long_window, trading_fee):
    """SMA 기반 매매 전략을 시뮬레이션합니다."""
    trades = []
    in_position = False
    capital = initial_capital
    buy_price = 0

    for i in range(1, len(df)):
        close_price = df['Close'].iloc[i]
        current_time = df['Time'].iloc[i]
        position_signal = df['Positions'].iloc[i]
        short_ma_value = df[f'short_MA'].iloc[i]
        long_ma_value = df[f'long_MA'].iloc[i]

        # 매수 조건: Positions 값이 1이고 포지션이 없는 경우
        if position_signal == 1 and not in_position:
            buy_price, quantity, capital = calculate_buy_order(close_price, capital, trading_fee)
            in_position = True
            trades.append(('buy', current_time, close_price, short_ma_value, long_ma_value, quantity, capital, None, None))

        # 매도 조건: Positions 값이 -1이고 포지션이 있는 경우
        elif position_signal == -1 and in_position:
            sell_price, capital, profit, return_rate = calculate_sell_order(close_price, buy_price, quantity, capital, trading_fee)
            in_position = False
            trades.append(('sell', current_time, close_price, short_ma_value, long_ma_value, quantity, capital, profit, return_rate))
    
    
    trades_df = pd.DataFrame(trades, columns=['Action', 'Time', 'Close', f'{short_window}MA', f'{long_window}MA', 'Quantity', 'Capital', 'Profit', 'Return Rate (%)'])
    trades_df = trades_df.fillna('')  # NaN 값을 빈 문자열로 대체

    return trades_df


def golden_cross_backtest(ticker="VOO", count=30, initial_capital=10000, window_combinations=[[5, 20]], trading_fee=0):
    """특정 심볼에 대한 SMA 기반 백테스트 실행"""
    results = []

    for short_window, long_window  in window_combinations:
        df = load_data(f'{ticker}_history.csv', count + long_window)

        df = calculate_short_long_moving_averages(df, short_window, long_window)
        df = df.tail(count)

        df = signal_positions_golden_corss(df, short_window, long_window)

        # 매매 시뮬레이션 실행
        trades_df = golden_cross_trading_simulation(df, initial_capital, short_window, long_window, trading_fee)

        # 각 트랜잭션 기록 저장
        save_trades_to_file(trades_df, f'Golden_Cross/Golden_Cross_{ticker}', f'Golden_Cross_{ticker}_{short_window}_{long_window}MA')

        # 성과 계산 및 'Window' 열 추가
        first_date, last_date = extract_periods(df)
        performance_df = calculate_performance(trades_df, initial_capital, first_date, last_date)
        performance_df.insert(0, 'Window', f"{short_window}_{long_window}")

        results.append(performance_df)

    return results



def golden_backtest_batch_run(tickers=["VOO"], count=10, capital=10000, window_combinations=[(5, 20)], fee=0):
    results = {}
    for ticker in tickers:
        backtest_df = golden_cross_backtest(ticker, count, capital, window_combinations, fee)

        # # 각 결과들을 하나의 DataFrame으로 합치기
        performance_df = pd.concat(backtest_df, ignore_index=True)

        # # 성과 요약 저장
        save_performance_to_file(performance_df, 'Golden_Cross', f'Golden_Cross_{ticker}')

        results[ticker] = performance_df

    return results



if __name__ == "__main__":
    tickers = TICKERS
    count = 365
    capital = 10000
    window_combinations = [(5, 20), (5, 40), (10, 20), (10, 40)]  
    fee = 0.001

    # 백테스트 실행
    results = golden_backtest_batch_run(tickers, count, capital, window_combinations, fee)

    # 결과 출력
    output = format_backtest_results(results, "Golden Cross Backtest", count)
    print(output)
