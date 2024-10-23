import sys
import yfinance as yf
from datetime import datetime, timedelta
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.config.constants import DATA_PATH, TICKERS


def save_ticker_data_to_csv(ticker_symbol, days):
    """
    주어진 티커명과 일수에 대한 데이터를 가져와 CSV로 저장하는 함수.
    
    :param ticker_symbol: 주식 또는 ETF 티커 심볼 (예: 'QQQ', 'VOO')
    :param days: 가져올 과거 일수 (예: 100)
    """
    # Ticker 데이터 불러오기
    ticker = yf.Ticker(ticker_symbol)

    # 오늘 날짜와 지정한 일수 전 날짜 계산
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')

    # 티커의 과거 데이터를 가져오기
    ticker_history = ticker.history(start=start_date, end=end_date)
    ticker_history = ticker_history.reset_index().rename(columns={'Date': 'Time'})

    # 파일 저장 경로
    directory = DATA_PATH
    csv_filename = f"{ticker_symbol}_history.csv"
    csv_path = os.path.join(directory, csv_filename)

    # 디렉토리가 없으면 생성
    if not os.path.exists(directory):
        os.makedirs(directory)

    # CSV 파일로 저장
    ticker_history.to_csv(csv_path)
    
    print(f"Data saved to {csv_path}")


# 함수 실행 예시
if __name__ == "__main__":
    # tickers = TICKERS
    tickers = ["SKYY"]

    count = 365
    for ticker in tickers:
        save_ticker_data_to_csv(ticker, count)
   

   
