import sys
import os
import pandas as pd

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)

from v2.apis.yfinance_history import save_ticker_data_to_csv
from v2.backtest.sma_backtest import sma_backtest_batch_run
from v2.backtest.goden_cross_backtest import golden_backtest_batch_run
from v2.config.constants import RESULT_ANALYSIS_PATH, RESULT_BACKTEST_PATH, RESULT_PERFORMANCE_PATH, TICKERS


def fetch_ticker_data(tickers, count=1000):
    """티커 데이터를 저장합니다."""
    for ticker in tickers:
        save_ticker_data_to_csv(ticker, count)


def run_backtests(tickers, count=365, capital=10000, windows=[5, 20, 60, 120], window_combinations=[(5, 20), (5, 40), (10, 20), (10, 40)], fee=0.001):
    """SMA와 Golden Cross 백테스트를 실행합니다."""
    sma_backtest_batch_run(tickers, count, capital, windows, fee)
    golden_backtest_batch_run(tickers, count, capital, window_combinations, fee)


def evaluate_backtest_results(tickers):
    """백테스트 결과를 평가하고, 최고 전략과 마지막 시그널을 찾아 출력 및 저장합니다."""
    strategies = ['SMA', 'Golden_Cross']
    total_string = ''
    results_list = []

    for ticker in tickers:
        ticker_returns = []  # 각 ticker의 전략별 성과를 저장할 리스트

        ticker_header = f"\n\n* {ticker} _____________"
        total_string += ticker_header

        for strategy in strategies:
            strategy_header = f"\n| {strategy}\n"
            total_string += strategy_header

            # 성과 파일 로드
            performance_file = f'{RESULT_PERFORMANCE_PATH}/{strategy}/performance_{strategy}_{ticker}.csv'
            performance_df = pd.read_csv(performance_file)
            df_string = performance_df.to_string(index=False, justify='center', col_space=15) + '\n'
            total_string += df_string

            # 'Return (%)'의 최대값과 그에 해당하는 'Window' 값 찾기
            max_return_idx = performance_df['Return (%)'].idxmax()  # 최대값의 인덱스
            max_return = performance_df['Return (%)'].iloc[max_return_idx]
            max_window = performance_df['Window'].iloc[max_return_idx]

            # 마지막 시그널 가져오기
            last_signal = performance_df['Action'].iloc[-1] if 'Action' in performance_df.columns else 'No Signal'

            # 해당 ticker의 성과 저장
            ticker_returns.append({
                'Strategy': strategy,
                'Window': max_window,
                'Return': max_return,
                'Last Signal': last_signal
            })

        # 각 티커에서 최대 Return을 가진 전략 및 Window 찾기
        # backtest 파일 경로 설정
        backtest_path = os.path.join(RESULT_BACKTEST_PATH, f'{strategy}/{strategy}_{ticker}/backtest_{strategy}_{ticker}_{max_window}MA.csv')
        backtest_df = pd.read_csv(backtest_path)

        # 마지막 행의 'Action', 'Time', 'Close' 값 가져오기
        last_row = backtest_df.iloc[-1]  # 마지막 행
        last_action = last_row['Action']
        last_time = last_row['Time']
        last_close = last_row['Close']

        max_return_strategy = max(ticker_returns, key=lambda x: x['Return'])

        # Best strategy 저장
        results_list.append({
            'Ticker': ticker,
            'Best Strategy': max_return_strategy['Strategy'],
            'Window': max_return_strategy['Window'],
            'Return (%)': max_return_strategy['Return'],
            'Last Signal': max_return_strategy['Last Signal'],
            'Last Action': last_action,
            'Last Time': last_time,
            'Last Price': last_close
        })

    # 백테스트 평가 결과 파일 저장 및 출력
    save_to_file(total_string, 'backtest_evaluation.txt')
    print(total_string)

    # Best strategy DataFrame 생성 및 출력
    results_df = pd.DataFrame(results_list)
    print(f"\n{results_df}")

    # Best strategy 결과 파일로 저장
    results_df.to_csv(os.path.join(RESULT_ANALYSIS_PATH, 'backtest_best_strategy.txt'), sep='\t', index=False)



def save_to_file(content, filename):
    """파일로 저장하는 함수"""
    output_file = os.path.join(RESULT_ANALYSIS_PATH, filename)
    with open(output_file, 'w') as f:
        f.write(content)


def main_backtest_process(tickers):
    """백테스트 실행 및 평가 메인 함수"""
    # fetch_ticker_data(tickers)  # 티커 데이터 저장
    # run_backtests(tickers)  # 백테스트 실행
    evaluate_backtest_results(tickers)  # 백테스트 평가


if __name__ == "__main__":
    tickers = TICKERS
    main_backtest_process(tickers)