import yfinance as yf

def get_stock_name(ticker_code):
    """
    yfinance를 사용하여 종목 코드로 종목 이름을 조회하는 함수.
    
    Args:
        ticker_code (str): 종목 코드 (예: '005930.KS' - 삼성전자)
    
    Returns:
        str: 종목 이름
    """
    stock = yf.Ticker(ticker_code)
    stock_info = stock.info  # 종목의 메타데이터
    
    if 'longName' in stock_info:
        return stock_info['longName']
    else:
        print(f"종목 이름을 찾을 수 없습니다: {ticker_code}")
        return None

if __name__ == "__main__":
    ticker_code = "102110.KS"  
    stock_name = get_stock_name(ticker_code)
    
    if stock_name:
        print(f"종목 코드 {ticker_code}의 이름은 {stock_name}입니다.")
