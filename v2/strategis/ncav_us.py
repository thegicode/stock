
import os
import sys
import yfinance as yf
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가


from v2.config.constants import TICKERS

def get_ncav_candidates_us(tickers):
    """
    해외 종목 NCAV 전략에 맞는 종목 후보군을 찾는 함수.
    Parameters:
    - tickers (list): 분석할 주식 티커 리스트
    Returns:
    - DataFrame: 조건에 맞는 종목과 관련 데이터
    """
    ncav_candidates = []
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        
        # 시가총액
        market_cap = stock.info.get('marketCap', None)
        
        # 재무제표 데이터 가져오기
        balance_sheet = stock.quarterly_balance_sheet
        financials = stock.quarterly_financials

        # 유동자산과 총부채
        current_assets = balance_sheet.loc['Total Current Assets'].iloc[0] if 'Total Current Assets' in balance_sheet.index else None
        total_liabilities = balance_sheet.loc['Total Liab'].iloc[0] if 'Total Liab' in balance_sheet.index else None
        
        # 분기 순이익
        net_income = financials.loc['Net Income'].iloc[0] if 'Net Income' in financials.index else None
        
        if current_assets and total_liabilities and market_cap and net_income:
            # 조건 필터링
            if (current_assets - total_liabilities) > market_cap and net_income > 0:
                ncav_ratio = (current_assets - total_liabilities) / market_cap
                ncav_candidates.append({
                    'Ticker': ticker,
                    'Market Cap': market_cap,
                    'Current Assets': current_assets,
                    'Total Liabilities': total_liabilities,
                    'Net Income': net_income,
                    'NCAV Ratio': ncav_ratio
                })
    
    # NCAV 후보군이 비어있는지 확인
    if ncav_candidates:
        # DataFrame으로 변환 후 NCAV 비율로 정렬
        return pd.DataFrame(ncav_candidates).sort_values(by='NCAV Ratio', ascending=False)
    else:
        print("조건에 맞는 종목이 없습니다.")
        return pd.DataFrame()  # 빈 DataFrame 반환


if __name__ == "__main__":  
    # 예시 사용
    tickers = TICKERS  # 분석할 종목 리스트
    ncav_stocks = get_ncav_candidates_us(tickers)

    # 결과 출력
    if not ncav_stocks.empty:
        print(ncav_stocks)
    else:
        print("조건에 맞는 NCAV 종목이 없습니다.")
