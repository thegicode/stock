def calculate_moving_averages(df, window):
    """이동 평균을 계산하여 데이터프레임에 추가합니다."""
    df[f'{window}MA'] = df['Close'].rolling(window=window).mean()
    return df


def calculate_short_long_moving_averages(df, short_window=50, long_window=200):
    df['short_MA'] = df['Close'].rolling(window=short_window).mean()
    df['long_MA'] = df['Close'].rolling(window=long_window).mean()
    return df


def signal_positions_sma(df, window):
    # 기본 신호 값 설정
    df['Positions'] = 0

    # 이동 평균의 변화에 따른 매수 및 매도 신호 생성
    df.loc[df[f'Close'] > df[f'{window}MA'], 'Positions'] = 1  # 종가가 이동평균보다 높으면 매수
    df.loc[df[f'Close'] < df[f'{window}MA'], 'Positions'] = -1  # 종가가 이동평균보다 낮으면 매도

    return df


def signal_positions_golden_corss(df, short_window, long_window):
    df['Positions'] = 0

    # 매수 조건: 단기 이동평균이 장기 이동평균을 상향 돌파
    df.loc[df[f'short_MA'] > df[f'long_MA'], 'Positions'] = 1  

    # 매도 조건: 단기 이동평균이 장기 이동평균을 하향 돌파
    df.loc[df[f'short_MA'] < df[f'long_MA'], 'Positions'] = -1 

    return df