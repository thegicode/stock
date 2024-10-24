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

        # 'X'로만 채워진 열을 확인할 열 목록을 지정합니다. 예: 불성실공시, 관리종목 등
        # cols_to_check = ['매매거래정지', '정리매매 종목', '관리종목', '투자주의환기종목', '불성실공시']

        filtered_stocks = df[df.apply(lambda row: (row != 'O').all(), axis=1)]

        return filtered_stocks

    except UnicodeDecodeError:
        print("파일을 읽는 중 인코딩 오류가 발생했습니다.")
        return None
    

if __name__ == "__main__":  
    result = filter_kor_stocks_by_validation()
    print(result)
