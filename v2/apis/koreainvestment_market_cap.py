
import os
import sys
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)

from v2.config.get_key import ACCESS_TOKEN, CLIENT_KEY, CLIENT_SECRET
from v2.config.constants import KOREA_INVESTMENT_URL


def get_market_cap_kor(ticker):
    """한국투자증권 API를 사용해 특정 종목의 시가총액을 계산하는 함수"""
    url = f"{KOREA_INVESTMENT_URL}/uapi/domestic-stock/v1/quotations/inquire-price"
    headers = {
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appkey": CLIENT_KEY,
        "appsecret": CLIENT_SECRET,
        "tr_id": "FHKST01010100"  # 시세 정보 조회 트랜잭션 ID
    }
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",  # 시장 구분 코드 (J: KOSPI, K: KOSDAQ)
        "FID_INPUT_ISCD": ticker  # 종목 코드 (예: '005930' for 삼성전자)
    }

    response = requests.get(url, headers=headers, params=params)

    # 상태 코드 확인
    if response.status_code != 200:
        print(f"API 호출 실패: {response.status_code}")
        print(f"응답 내용: {response.text}")
        return None

    # JSON 파싱
    try:
        data = response.json()
    except ValueError:
        print("JSON 디코딩 에러: 응답이 비어있거나 올바르지 않은 형식입니다.")
        print(f"응답 내용: {response.text}")
        return None

    try:
        # 종가와 상장주식수 정보 추출
        stock_price = int(data['output']['stck_prpr'])  # 종가
        shares_outstanding = int(data['output']['lstn_stcn'])  # 상장주식수

        # 시가총액 계산
        market_cap = stock_price * shares_outstanding
        print(f"종목 코드: {ticker}, 시가총액: {market_cap}")
        return market_cap

    except KeyError:
        print(f"'{ticker}'의 시가총액 계산에 필요한 데이터가 누락되었습니다.")
        return None


if __name__ == "__main__":
    # 예시 종목 리스트 (삼성전자, SK하이닉스, NAVER)
    tickers = ['005930', '000660', '035420']
    
    for ticker in tickers:
        get_market_cap_kor(ticker)

