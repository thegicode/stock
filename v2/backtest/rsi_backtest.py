
import sys
import os
import pandas as pd

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)

from v2.config.constants import TICKERS
from v2.utils.file_utils import load_data, save_performance_to_file
from v2.utils.finantial_utils import calculate_rsi, signal_positions_rsi
from v2.utils.trade_utils import generic_trading_simulation
from v2.utils.performance_utils import format_backtest_results, save_and_evaluate_performance


STRATEGE_NAME = 'RSI'


def rsi_trading_simulation(df, initial_capital, window, trading_fee):
    return generic_trading_simulation(df, initial_capital, trading_fee, position_col='Positions', ma_cols=[f'RSI'])


def rsi_backtest(ticker="VOO", count=30, initial_capital=10000, windows=[6, 12,  14, 18, 24, 30], overbought=75, oversold=25, trading_fee=0.001):
    """특정 심볼에 대한 SMA 기반 백테스트 실행"""
    results = []
    for window in windows:
        df = load_data(f'{ticker}_history.csv', count + window)

        df = calculate_rsi(df, window)
        df = df.tail(count)

        df = signal_positions_rsi(df, overbought, oversold)

        # # 매매 시뮬레이션 실행
        trades_df = rsi_trading_simulation(df, initial_capital, window, trading_fee)

        # # 성과 계산 및 저장 함수 호출
        performance_df = save_and_evaluate_performance(trades_df, df, initial_capital, STRATEGE_NAME, ticker, f"{window}")

        results.append(performance_df)

    return results

# 여러 티커에 대한 백테스트 실행

def rsi_backtest_batch_run(tickers=["VOO"], count=10, capital=10000, windows=[6, 12,  14, 18, 24, 30], overbought=75, oversold=25, fee=0.001):
    results = {}
    for ticker in tickers:
        backtest_df = rsi_backtest(ticker, count, capital, windows, overbought, oversold, fee)

        # # 각 결과들을 하나의 DataFrame으로 합치기
        performance_df = pd.concat(backtest_df, ignore_index=True)

        # # 성과 요약 저장
        save_performance_to_file(performance_df, STRATEGE_NAME, f'{STRATEGE_NAME}_{ticker}')

        results[ticker] = performance_df

    return results



if __name__ == "__main__":
    # tickers = TICKERS
    tickers=["VOO"]
    count = 365
    capital = 10000
    windows=[6, 12,  14, 18, 24, 30]
    overbought=75 
    oversold=25
    fee = 0.001

    # 백테스트 실행
    results = rsi_backtest_batch_run(tickers, count, capital, windows, overbought, oversold, fee)

    # 결과 출력
    output = format_backtest_results(results, f"{STRATEGE_NAME} Backtest", count)
    print(output)
