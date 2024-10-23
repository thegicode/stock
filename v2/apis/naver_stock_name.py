import requests
from bs4 import BeautifulSoup

def get_stock_name_from_naver(ticker_code):
    """
    네이버 금융에서 종목 번호로 종목 이름을 가져오는 함수.
    
    Args:
        ticker_code (str): 종목 번호 (예: '005930' - 삼성전자)
    
    Returns:
        str: 종목 이름 또는 None
    """
    url = f"https://finance.naver.com/item/main.nhn?code={ticker_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 종목 이름을 포함하는 태그 추출
        stock_name_tag = soup.find('div', {'class': 'wrap_company'}).find('h2')
        
        if stock_name_tag:
            stock_name = stock_name_tag.text.strip()
            return stock_name
        else:
            print(f"종목 이름을 찾을 수 없습니다: {ticker_code}")
            return None
    else:
        print(f"HTTP 요청 오류: {response.status_code}")
        return None

if __name__ == "__main__":
    ticker_code = "005930"  # 삼성전자 종목 코드
    stock_name = get_stock_name_from_naver(ticker_code)
    
    if stock_name:
        print(f"종목 코드 {ticker_code}의 이름은 {stock_name}입니다.")
    else:
        print(f"종목 코드 {ticker_code}의 이름을 찾을 수 없습니다.")
