def calculate_moving_averages(df, window):
    """이동 평균을 계산하여 데이터프레임에 추가합니다."""
    df[f'{window}MA'] = df['Close'].rolling(window=window).mean()
    return df


def calculate_short_long_moving_averages(df, short_window=50, long_window=200):
    df['short_MA'] = df['Close'].rolling(window=short_window).mean()
    df['long_MA'] = df['Close'].rolling(window=long_window).mean()
    return df


def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    """MACD와 신호선을 계산합니다."""
    df['EMA_short'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal Line']
    return df


def calculate_rsi(df, window=14):
    """RSI 계산."""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def calculate_bollinger_bands(df, window=20, num_std_dev=2):
    """볼린저 밴드를 계산하여 데이터프레임에 추가합니다."""
    df['Middle Band'] = df['Close'].rolling(window=window).mean()
    df['Std Dev'] = df['Close'].rolling(window=window).std()
    df['Upper Band'] = df['Middle Band'] + (df['Std Dev'] * num_std_dev)
    df['Lower Band'] = df['Middle Band'] - (df['Std Dev'] * num_std_dev)
    return df


def signal_positions_sma(df, window):
    # 기본 신호 값 설정
    df['Positions'] = 0

    # 이동 평균의 변화에 따른 매수 및 매도 신호 생성
    df.loc[df[f'Close'] > df[f'{window}MA'], 'Positions'] = 1  # 종가가 이동평균보다 높으면 매수
    df.loc[df[f'Close'] < df[f'{window}MA'], 'Positions'] = -1  # 종가가 이동평균보다 낮으면 매도

    return df


def signal_positions_golden_corss(df):
    df['Positions'] = 0

    # 매수 조건: 단기 이동평균이 장기 이동평균을 상향 돌파
    df.loc[df[f'short_MA'] > df[f'long_MA'], 'Positions'] = 1  

    # 매도 조건: 단기 이동평균이 장기 이동평균을 하향 돌파
    df.loc[df[f'short_MA'] < df[f'long_MA'], 'Positions'] = -1 

    return df



def signal_positions_macd(df):
    df['Positions'] = 0

    # 매수 조건: MACD가 Signal 위로 올라가면 매수
    df.loc[df[f'MACD'] > df[f'Signal Line'], 'Positions'] = 1  

    # 매도 조건: MACD가 Signal 아래로 내려가면 매도
    df.loc[df[f'MACD'] < df[f'Signal Line'], 'Positions'] = -1 

    return df


def signal_positions_rsi(df, overbought=75, oversold=25):
    # 기본 신호 값 설정
    df['Positions'] = 0

    # 이동 평균의 변화에 따른 매수 및 매도 신호 생성
    df.loc[df[f'RSI'] < oversold, 'Positions'] = 1  # 종가가 이동평균보다 높으면 매수
    df.loc[df[f'RSI'] > overbought, 'Positions'] = -1  # 종가가 이동평균보다 낮으면 매도

    return df


def signal_positions_bollinger(df):
    """
    불린저 밴드 기반의 매수/매도 시그널을 생성하는 함수.
    
    Args:
        df (pd.DataFrame): 불린저 밴드가 포함된 데이터프레임
    
    Returns:
        pd.DataFrame: 매수/매도 시그널이 추가된 데이터프레임
    """
    df['Positions'] = 0

    # 매수 조건: 현재 주가가 하단 밴드 위로 올라오고, 이전 주가는 하단 밴드보다 작을 때
    df.loc[(df['Close'] > df['Lower Band']) & (df['Close'].shift(1) <= df['Lower Band'].shift(1)), 'Positions'] = 1

    # 매도 조건: 현재 주가가 상단 밴드 아래로 내려가고, 이전 주가는 상단 밴드보다 클 때
    df.loc[(df['Close'] < df['Upper Band']) & (df['Close'].shift(1) >= df['Upper Band'].shift(1)), 'Positions'] = -1

    return df

