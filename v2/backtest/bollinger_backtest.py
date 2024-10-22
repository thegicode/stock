import sys
import os
import pandas as pd

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)

from v2.utils.finantial_utils import calculate_bollinger_bands, calculate_moving_averages, signal_positions_bollinger, signal_positions_sma
from v2.utils.trade_utils import calculate_buy_order, calculate_sell_order, generic_trading_simulation
from v2.utils.performance_utils import calculate_performance, format_backtest_results, save_and_evaluate_performance
from v2.utils.file_utils import load_data, save_performance_to_file, save_trades_to_file
from v2.utils.time_utils import extract_periods
from v2.config.constants import TICKERS


STRATEGE_NAME = 'Bollinger'

def bollinger_trading_simulation(df, initial_capital, window, trading_fee):
    return generic_trading_simulation(df, initial_capital, trading_fee, position_col='Positions', ma_cols=['Upper Band', 'Lower Band'])


def bollinger_backtest(ticker="VOO", count=30, initial_capital=10000, windows=[20], num_std_dev=0.2, trading_fee=0.001):
    """특정 심볼에 대한 SMA 기반 백테스트 실행"""
    results = []
    for window in windows:
        df = load_data(f'{ticker}_history.csv', count + window)
        
        df = calculate_bollinger_bands(df, window, num_std_dev)
        df = df.tail(count)

        df = signal_positions_bollinger(df)

        # 매매 시뮬레이션 실행
        trades_df = bollinger_trading_simulation(df, initial_capital, window, trading_fee)

        # # 성과 계산 및 저장 함수 호출
        performance_df = save_and_evaluate_performance(trades_df, df, initial_capital, STRATEGE_NAME, ticker, f"{window}")

        results.append(performance_df)

    return results


def bollinger_backtest_batch_run(tickers=["VOO"], count=10, capital=10000, windows=[20], num_std_dev=2, fee=0.001):
    results = {}
    for ticker in tickers:
        backtest_df = bollinger_backtest(ticker, count, capital, windows, num_std_dev, fee)

        # 각 결과들을 하나의 DataFrame으로 합치기
        performance_df = pd.concat(backtest_df, ignore_index=True)

        # 성과 요약 저장
        save_performance_to_file(performance_df, STRATEGE_NAME, f'{STRATEGE_NAME}_{ticker}')

        results[ticker] = performance_df

    return results



if __name__ == "__main__":
    tickers = TICKERS
    count = 365
    capital = 10000
    windows = [20, 30, 60]
    num_std_dev = 2
    fee = 0.001

    # 백테스트 실행
    results = bollinger_backtest_batch_run(tickers, count, capital, windows, num_std_dev, fee)

    # 결과 출력
    output = format_backtest_results(results, f"{STRATEGE_NAME} Backtest", count)
    print(output)
