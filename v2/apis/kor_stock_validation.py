import os
import sys
import pandas as pd

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.config.constants import DATA_KOR_PATH
from v2.apis.kor_stock_list_loader import get_kor_stock_list


def filter_kor_stocks_by_validation(stocks=None):
    """
    지정된 CSV 파일을 읽고, stocks 리스트와 비교하여
    지정된 열이 모두 'X'인 행만 필터링하는 함수.
    DATA : http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201
        전종목 지정종목
    """
    if stocks is None:
        # 국내 종목 리스트 가져오기
        stocks = get_kor_stock_list()

    #  다운로드한 CSV 파일 경로
    file_path = os.path.join(DATA_KOR_PATH, 'kor_stock_specified.csv')

    # CSV 파일을 읽을 때 인코딩을 'cp949'로 설정 (필요에 따라 'euc-kr'로 변경 가능)
    try:
        df = pd.read_csv(file_path, encoding='cp949')

        # '종목코드'를 기준으로 stocks에서 없는 종목을 필터링
        df['종목코드'] = df['종목코드'].astype(str)  # 종목코드 형식을 맞춰줌 (필요시)

        # 'X'로만 채워진 열을 확인하여 필터링
        filtered_stocks = df[df.apply(lambda row: (row != 'O').all(), axis=1)]

        # '종목코드', '종목명'만 남기고 나머지 열 삭제
        filtered_stocks = filtered_stocks[['종목코드', '종목명']]

        # stocks 데이터에서 '단축코드'가 일치하는 행을 가져옴
        stocks['단축코드'] = stocks['단축코드'].astype(str)  # 단축코드 형식을 맞춤
        merged_stocks = pd.merge(filtered_stocks, stocks, left_on='종목코드', right_on='단축코드', how='inner')

        # 병합된 데이터에서 '종목코드', '종목명', '단축코드' 등 필요한 열만 선택
        final_stocks = merged_stocks[['종목코드', '표준코드', '종목명', '한글 종목명', '상장일', '시장구분', '주식종류', '액면가', '상장주식수']]

        # 파일 저장
        csv_path = os.path.join(DATA_KOR_PATH, 'kor_stock_filtered.csv')
        final_stocks.to_csv(csv_path, index=False, encoding='utf-8-sig')  # 파일 저장 경로 및 인코딩 지정

        print(f"Data saved to {csv_path}, {len(final_stocks)} 종목")

        return final_stocks

    except UnicodeDecodeError:
        print("파일을 읽는 중 인코딩 오류가 발생했습니다.")
        return None
    

if __name__ == "__main__":  
    result = filter_kor_stocks_by_validation()
    print(result)
