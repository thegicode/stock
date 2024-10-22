import sys
import os
import pandas as pd

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)

from v2.utils.file_utils import load_data, save_performance_to_file, save_trades_to_file
from v2.config.constants import TICKERS
from v2.utils.performance_utils import calculate_performance, format_backtest_results, save_and_evaluate_performance
from v2.utils.finantial_utils import calculate_short_long_moving_averages, signal_positions_golden_corss
from v2.utils.time_utils import extract_periods
from v2.utils.trade_utils import calculate_buy_order, calculate_sell_order, generic_trading_simulation


STRATEGE_NAME = 'Golden_Cross'


def golden_cross_trading_simulation(df, initial_capital, short_window, long_window, trading_fee):
    return generic_trading_simulation(df, initial_capital, trading_fee, position_col='Positions', ma_cols=[f'short_MA', f'long_MA'])


def golden_cross_backtest(ticker="VOO", count=30, initial_capital=10000, window_combinations=[[5, 20]], trading_fee=0.001):
    """특정 심볼에 대한 SMA 기반 백테스트 실행"""
    results = []

    for short_window, long_window  in window_combinations:
        df = load_data(f'{ticker}_history.csv', count + long_window)

        df = calculate_short_long_moving_averages(df, short_window, long_window)
        df = df.tail(count)

        df = signal_positions_golden_corss(df)

        # 매매 시뮬레이션 실행
        trades_df = golden_cross_trading_simulation(df, initial_capital, short_window, long_window, trading_fee)

        # 성과 계산 및 저장 함수 호출
        performance_df = save_and_evaluate_performance(trades_df, df, initial_capital, STRATEGE_NAME, ticker, f"{short_window}_{long_window}")

        results.append(performance_df)

    return results


def golden_backtest_batch_run(tickers=["VOO"], count=10, capital=10000, window_combinations=[(5, 20)], fee=0.001):
    results = {}
    for ticker in tickers:
        backtest_df = golden_cross_backtest(ticker, count, capital, window_combinations, fee)

        # # 각 결과들을 하나의 DataFrame으로 합치기
        performance_df = pd.concat(backtest_df, ignore_index=True)

        # # 성과 요약 저장
        save_performance_to_file(performance_df, STRATEGE_NAME, f'{STRATEGE_NAME}_{ticker}')

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
    output = format_backtest_results(results, f"{STRATEGE_NAME} Backtest", count)
    print(output)
