import os
import sys
from dotenv import load_dotenv
import requests
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.config.constants import DATA_KOR_PATH
from v2.config.get_key import ACCESS_TOKEN, CLIENT_KEY, CLIENT_SECRET

def format_time_column(df):
    """
    'Time' 열을 'YYYY-MM-DD HH:MM:SS-TZ' 형식으로 변환한 후, 과거 데이터가 먼저 오도록 정렬하는 함수.
    
    Args:
        df (pd.DataFrame): 시간 데이터가 포함된 DataFrame
    
    Returns:
        pd.DataFrame: 변환 및 정렬된 시간 데이터
    """
    # 'Time' 열을 날짜 형식으로 변환 (예: '20241022' -> '2024-10-22')
    df['Time'] = pd.to_datetime(df['Time'], format='%Y%m%d')

    # 원하는 타임존 설정 (-05:00 시간대)
    df['Time'] = df['Time'].dt.tz_localize('UTC').dt.tz_convert('America/New_York')

    # 'Time' 열을 기준으로 오름차순(과거 데이터가 먼저 오도록) 정렬
    df = df.sort_values(by='Time', ascending=True)

    return df


def koreainvest_save_ticker_data_to_csv(ticker_code, max_records=1000):
    """
    ACE 미국 S&P500 ETF의 최대 일별 데이터를 가져오는 함수.

    Parameters:
    ticker_code (str): 조회할 종목 코드 (예: 305540)
    max_records (int): 최대 조회할 레코드 수

    Returns:
    DataFrame: 일별 데이터의 DataFrame
    """
    
    url = "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-daily-price"
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appkey": CLIENT_KEY,
        "appsecret": CLIENT_SECRET,
        "tr_id": "FHKST01010400"  # 일봉 데이터 조회
    }
    
    all_data = []  # 모든 데이터를 저장할 리스트
    count = 0      # 현재 조회된 레코드 수

    # 데이터 조회 반복
    while count < max_records:
        # 요청 파라미터 설정 (최근 날짜부터 조회)
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 시장 구분 코드 (J: ETF)
            "FID_INPUT_ISCD": ticker_code,  # 종목 코드
            "FID_PERIOD_DIV_CODE": "D",     # 기간 구분 (D: 일)
            "FID_ORG_ADJ_PRC": "0",         # 수정 주가 (0: 비조정, 1: 수정주가)
            "FID_COUNT": "100",             # 요청 레코드 수 (최대 100개)
            "FID_START_DATE": "YYYYMMDD"    # 시작 날짜 (API 문서 참고)
        }
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if 'output' in data:
            all_data.extend(data['output'])
            count += len(data['output'])

            if len(data['output']) < 100:
                # 받은 데이터가 100개 미만이면 더 이상 데이터가 없음
                break
        else:
            print("데이터를 가져오는 데 실패했습니다:", data)
            break

    # DataFrame으로 변환
    df = pd.DataFrame(all_data)
    display_columns = ['stck_bsop_date', 'stck_clpr', 'stck_oprc', 'stck_hgpr', 'stck_lwpr', 'acml_vol']
    df = df[display_columns]
    df.columns = ['Time', 'Close', 'Open', 'High', 'Low', 'Volume']
    df = format_time_column(df)

    csv_file_path = f'{DATA_KOR_PATH}/{ticker_code}_history.csv'
    df.to_csv(csv_file_path, index=True)
    print(f"데이터가 '{csv_file_path}' 파일로 저장되었습니다.")

    return df


if __name__ == "__main__":  
    # 사용 예시
    ticker_code = "305540"  # ACE 미국 S&P500 ETF 코드
    daily_data = koreainvest_save_ticker_data_to_csv(ticker_code, max_records=1000)  # 원하는 최대 레코드 수 지정
    print(daily_data)
