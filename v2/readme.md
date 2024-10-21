# 실행

cd /Users/deokim/Documents/코딩/project-my/stock
source venv/bin/activate

# 초기 설치

python3 -m venv venv
requirements.txt

---

# 함수

## apis

데이터 다운
python3 v2/apis/yfinance_history.py

## Backtest

Backtest Runner
python3 v2/backtest/backtest_runner.py

SMA
python3 v2/backtest/sma_backtest.py

Golden Cross
python3 v2/backtest/goden_cross_backtest.py

# 해외 주식 api

-   [Alpha Vantage](https://www.alphavantage.co/documentation/)
-   [Yahoo Finance](https://www.financeapi.net)
-   [Google Finance](https://serpapi.com/google-finance-api)
-   Quandl

## 백테스트 결과

-   테슬라 : 20일 이동평균
-   엔비디아 : 120일 이동평균
