import os
import sys
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.config.constants import DATA_KOR_PATH


def get_kor_stock_list():
    """
    KOSPI 종목 리스트를 CSV 파일에서 가져오는 함수.
    DATA : http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201 
        전종목 기본정보
    """
    # 다운로드한 CSV 파일 경로
    file_path = os.path.join(DATA_KOR_PATH, 'kor_stock_list.csv')

    # CSV 파일을 읽을 때 인코딩을 'cp949'로 설정 (필요에 따라 'euc-kr'로 변경 가능)
    try:
        df = pd.read_csv(file_path, encoding='cp949')
        return df
    except UnicodeDecodeError:
        print("파일을 읽는 중 인코딩 오류가 발생했습니다.")
        return None
    

if __name__ == "__main__":  
    # KOSPI 종목 리스트 가져오기
    kor_stock_df = get_kor_stock_list()
    if kor_stock_df is not None:
        print(kor_stock_df.head())


