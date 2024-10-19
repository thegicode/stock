import pandas as pd

def extract_periods(df):
    # 'Time' 열을 datetime 형식으로 변환
    df['Time'] = pd.to_datetime(df['Time'])

    # 첫 번째와 마지막 날짜 추출 및 포맷 변환
    first_date = df['Time'].iloc[0].strftime('%Y-%m-%d')
    last_date = df['Time'].iloc[-1].strftime('%Y-%m-%d')
    
    return first_date, last_date
