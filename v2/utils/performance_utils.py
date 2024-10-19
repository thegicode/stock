
import sys
import os
import pandas as pd
# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.utils.time_utils import extract_periods


def calculate_performance(trades_df, initial_capital, first_date, last_date ):
    """매매 전략의 성과 지표를 계산합니다."""

    trade_count = calculate_trade_count(trades_df)

    total_profit, total_returns = calculate_total_returns(trades_df, initial_capital)

    win_rate = calculate_win_rate(trades_df)

    mdd_percent = binance_calculate_mdd(trades_df, initial_capital)

    performance =  {
        'Trades': trade_count,
        'Profit': total_profit,
        'Return (%)': total_returns,
        'Win Rate (%)': win_rate,
        'Max Drawdown (%)': mdd_percent,
        'Periods': f"{first_date} ~ {last_date}"
    }
    performance_df = pd.DataFrame([performance])

    return performance_df



def calculate_trade_count(trades_df):
    """
    거래 횟수를 계산하는 함수.

    :param trades_df: 거래 내역이 포함된 DataFrame
    :return: 총 거래 횟수 (매도 횟수)
    """
    # 'Action' 열에서 매도('sell') 이벤트를 찾음
    trade_count = trades_df[trades_df['Action'] == 'sell'].shape[0]

    return trade_count



def calculate_total_returns(trades_df, initial_capital):
    """총 수익과 총 수익률을 계산하는 함수"""

    # 'Profit' 열을 숫자로 변환, 숫자가 아닌 값은 NaN으로 변환
    trades_df['Profit'] = pd.to_numeric(trades_df['Profit'])

    # NaN 값을 0으로 대체
    trades_df['Profit'] = trades_df['Profit'].fillna(0)

    # 총 수익 계산
    total_profit = trades_df['Profit'].sum()

    # 총 수익률 계산
    total_returns = (total_profit / initial_capital) * 100

    return total_profit, total_returns




def calculate_win_rate(trades_df):
    """
    승률을 계산하는 함수

    :param trades_df: 거래 내역이 포함된 DataFrame
    :return: 승률 (%)
    """
    # 매도 거래만 필터링 (Action이 'sell'인 거래)
    sell_trades = trades_df[trades_df['Action'] == 'sell']

    # 이익이 발생한 매도 거래 (Profit > 0)
    winning_trades = sell_trades[sell_trades['Profit'] > 0]

    # 총 매도 거래 수와 이긴 거래 수 계산
    total_sell_trades = len(sell_trades)
    total_wins = len(winning_trades)

    # 승률 계산 (총 이긴 거래 수 / 총 매도 거래 수 * 100)
    win_rate = (total_wins / total_sell_trades * 100) if total_sell_trades > 0 else 0

    return win_rate


def binance_calculate_mdd(trades_df, initial_capital):
    """
    최대 낙폭(MDD)을 계산하는 함수

    :param trades_df: 거래 내역이 포함된 DataFrame, 'Capital' 열이 있어야 함
    :param initial_capital: 초기 자본
    :return: 최대 낙폭 (MDD, %)
    """
    drawdowns = []
    peak = initial_capital

    # 거래 기록을 순차적으로 탐색하여 매수/매도에 따른 드로우다운 계산
    for _, row in trades_df.iterrows():
        if row['Action'] == 'buy':
            # 자본금 최고점을 갱신 (매수 시점에서는 peak 갱신)
            peak = max(peak, row['Capital'])
        elif row['Action'] == 'sell':
            # 매도 시점에서 드로우다운 계산
            drawdown = (peak - row['Capital']) / peak if peak != 0 else 0
            drawdown = max(drawdown, 0)  # 음수 드로우다운 방지
            drawdowns.append(drawdown)

    # 최대 낙폭을 백분율로 변환
    max_drawdown = (max(drawdowns) * 100) if drawdowns else 0

    return max_drawdown



def format_backtest_results(backtest_results, backtest_name):
    """백테스트 결과를 포맷팅하여 출력"""
    output = "-" * 100
    output += f"\n{backtest_name}"

    for symbol, performance_df in backtest_results.items():
        # 심볼과 기간 출력
        output += f"\n\n{symbol}\n"
        # output += f"Period: {first_date} ~ {last_date}\n"

        # 필요한 열만 선택하여 문자열로 변환
        output += performance_df[['Window', 'Trades', 'Profit', 'Return (%)', 'Win Rate (%)', 'Max Drawdown (%)', 'Periods']].to_string(index=False)
        output += "\n"

    return output