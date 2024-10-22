
import sys
import os
import pandas as pd

# 프로젝트 루트 경로를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # 루트 경로로 설정
sys.path.append(project_root)  # 루트 경로를 sys.path에 추가

from v2.config.constants import DATA_PATH, RESULT_BACKTEST_PATH, RESULT_PERFORMANCE_PATH


def load_data(data_file_name, count=None):
    """파일에서 데이터를 로드합니다."""
    file_path = os.path.join(DATA_PATH, data_file_name)
    df = pd.read_csv(file_path)
    df['Time'] = pd.to_datetime(df['Time'], utc=True)
    # df = pd.read_csv(file_path, parse_dates=['Time'])
    # df['Close'] = df['Close'].astype(float)  # 데이터 타입 보정


    if count is not None:
        df = df.tail(count)
        df = df.reset_index(drop=True)

    return df


def save_trades_to_file(df, result_dir, file_name):
    """거래 데이터를 CSV 파일로 저장합니다."""
    if df.empty:
        return

    result_dir = os.path.join(RESULT_BACKTEST_PATH, result_dir)
    file_name = f'backtest_{file_name}.csv'

    # Ensure the result directory exists
    os.makedirs(result_dir, exist_ok=True)
    file_path = os.path.join(result_dir, file_name)
    # print(f"Save to : {file_path}")

    # Save to CSV
    df.to_csv(file_path, index=False)



# 성과 결과 저장
def save_performance_to_file(performance_df, result_dir, file_name):
    """성과 결과를 CSV 파일로 저장합니다."""
    result_dir = os.path.join(RESULT_PERFORMANCE_PATH, result_dir)
    file_name = f'performance_{file_name}.csv'

    # Ensure the result directory exists
    os.makedirs(result_dir, exist_ok=True)
    file_path = os.path.join(result_dir, file_name)

    # Save to CSV
    performance_df.to_csv(file_path, index=False)
