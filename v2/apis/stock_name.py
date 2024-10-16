import os
import sys
from dotenv import load_dotenv
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.config.get_key import ACCESS_TOKEN, CLIENT_KEY, CLIENT_SECRET

# 원하는 종목명 조회 실패

def get_stock_info(ticker_code):
    """
    종목 코드를 사용하여 종목의 시장명과 상품 유형을 가져오는 함수.

    Parameters:
    ticker_code (str): 조회할 종목 코드 (예: 305540)

    Returns:
    dict: 종목 정보 (시장명 및 상품 유형)
    """
   
    url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appkey": CLIENT_KEY,
        "appsecret": CLIENT_SECRET,
        "tr_id": "FHKST01010100"  # 현재가 및 기본 정보 조회
    }
    
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",  # 시장 구분 코드 (J: ETF)
        "FID_INPUT_ISCD": ticker_code   # 종목 코드
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if 'output' in data:
        stock_info = {
            "market_name": data['output'].get('rprs_mrkt_kor_name', 'N/A'),
            "product_type": data['output'].get('bstp_kor_isnm', 'N/A')
        }
        return stock_info
    else:
        print("데이터를 가져오는 데 실패했습니다:", data)
        return None
    

if __name__ == "__main__":
    # 사용 예시
    ticker_code = "305540"  # ACE 미국 S&P500 ETF 코드
    stock_info = get_stock_info(ticker_code)
    if stock_info:
        print("시장명:", stock_info["market_name"])
        print("상품 유형:", stock_info["product_type"])
