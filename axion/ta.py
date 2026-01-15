import pandas as pd
import numpy as np


# Rate of Change
def roc(df, column="close", period=10):
    roc = ((df[column] / df[column].shift(period) - 1) * 100).fillna(0)
    return roc

# Momentum
def mom(df, column="close", period=10):
    mom = df[column].diff(period)
    return mom

# Simple Moving Avg
def sma(df, column="close", period=14):
    sma = df[column].rolling(window=period, min_periods=1).mean()
    return sma

# Simple Moving Median
def smm(df, column="close", period=14):
    smm = df[column].rolling(window=period).median()
    return

# Smoothed Simple Moving Average
def ssma(df, column="close", period=14):
    initial_sma = df[column].rolling(window=period).mean()
    ssma = initial_sma.ewm(alpha=1/period, adjust=False).mean()
    return ssma

# Exponential Moving Avg
def ema(df, column="close", period=14):
    ema = df[column].ewm(span=period, adjust=False).mean()
    return ema

# Double Exponential Moving Average
def dema(df, column="close", period=14):
    ema = df[column].ewm(span=period, adjust=False).mean()
    dema = 2 * ema - ema.ewm(span=period, adjust=False).mean()
    return dema

# Triangular Moving Average
def trima(df, column="close", period=14):
    sma = df[column].rolling(window=period).mean()
    trima = sma.rolling(window=period).mean()
    return trima

# Average True Range
def atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

# Stochastic Oscillator %K and %D
def stochastic_oscillator(df, k_period=14, d_period=3):
    low_min = df['low'].rolling(window=k_period).min()
    high_max = df['high'].rolling(window=k_period).max()
    K = ((df['close'] - low_min) / (high_max - low_min)) * 100
    D = K.rolling(window=d_period).mean()
    return K, D

# Chande Momentum Oscillator
def cmo(df, column="close", period=20):
    delta = df[column].diff(1)
    up = delta.where(delta > 0, 0).rolling(window=period).sum()
    down = -delta.where(delta < 0, 0).rolling(window=period).sum()
    cmo = ((up - down) / (up + down)) * 100
    return cmo

# On Balance Volume
def obv(df):
    obv = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
    return obv

# Volume Price Trend
def vpt(df):
    vpt = ((df['volume'] * ((df['close'] - df['close'].shift(1)) / df['close'].shift(1))).cumsum())
    return vpt

# Volume-Weighted Average Price
def vwap(df, period=14):
    vwap = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
    return vwap

# Bollinger Bands
def bbands(df, column="close", period=20, num_std_dev=2):
    sma = df[column].rolling(window=period).mean()
    std_dev = df[column].rolling(window=period).std()
    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)
    return upper_band, sma, lower_band

# Keltner Channels
def kc(df, period=20, atr_period=10, multiplier=2):
    sma = df['close'].rolling(window=period).mean()
    atr_val = atr(df, period=atr_period)
    upper_channel = sma + (atr_val * multiplier)
    lower_channel = sma - (atr_val * multiplier)
    return upper_channel, sma, lower_channel

# Kaufman's Adaptive Moving Average
def kama(df, column="close", period=14, fast=14, slow=30):
    df['direction'] = df[column] - df[column].shift(period)
    df['volatility'] = df[column].diff().abs().rolling(window=period).sum()
    df['ER'] = df['direction'] / df['volatility']
    sc = ((df['ER'] * (2 / (fast + 1) - 2 / (slow + 1)) + 2 / (slow + 1)) ** 2).fillna(0)
    kama = [df[column].iloc[0]]
    for i in range(1, len(df)):
        kama.append(kama[-1] + sc.iloc[i] * (df[column].iloc[i] - kama[-1]))
    return pd.Series(kama, index=df.index)

# Vortex Indicator
def vi(df, period=14):
    TR = np.maximum(df['high'] - df['low'], np.maximum(abs(df['high'] - df['close'].shift(1)), abs(df['low'] - df['close'].shift(1))))
    TR_sum = TR.rolling(window=period).sum()

    VM_plus = abs(df['high'] - df['low'].shift(1))
    VM_minus = abs(df['low'] - df['high'].shift(1))

    VI_plus = VM_plus.rolling(window=period).sum() / TR_sum
    VI_minus = VM_minus.rolling(window=period).sum() / TR_sum

    return VI_plus, VI_minus


# Moving Average Convergence Divergence
def macd(df, column="close", fast_period=12, slow_period=26, signal_period=9):
    ema_fast = df[column].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow_period, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

# Williams %R
def williams_r(df, period=14):
    high_max = df['high'].rolling(window=period).max()
    low_min = df['low'].rolling(window=period).min()
    williams_r = -100 * (high_max - df['close']) / (high_max - low_min)
    return williams_r

# Average Directional Index
def adx(df, period=14):
    tr = atr(df, period=1)  # True Range
    plus_dm = df['high'].diff()
    minus_dm = df['low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    plus_dm_smooth = plus_dm.rolling(window=period).sum()
    minus_dm_smooth = abs(minus_dm.rolling(window=period).sum())
    plus_di = 100 * (plus_dm_smooth / tr)
    minus_di = 100 * (minus_dm_smooth / tr)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(window=period).mean()
    return adx

# Relative Strength Index
def rsi(df, column="close", period=14):
    delta = df[column].diff(1)
    gain = delta.where(delta > 0, 0).fillna(0)
    loss = -delta.where(delta < 0, 0).fillna(0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Ichimoku Cloud
def ichi(df):
    high_9 = df['high'].rolling(window=9).max()
    low_9 = df['low'].rolling(window=9).min()
    conversion_line = (high_9 + low_9) / 2

    high_26 = df['high'].rolling(window=26).max()
    low_26 = df['low'].rolling(window=26).min()
    base_line = (high_26 + low_26) / 2

    leading_span_a = ((conversion_line + base_line) / 2).shift(26)

    high_52 = df['high'].rolling(window=52).max()
    low_52 = df['low'].rolling(window=52).min()
    leading_span_b = ((high_52 + low_52) / 2).shift(26)

    lagging_span = df['close'].shift(-26)
    return conversion_line, base_line, leading_span_a, leading_span_b, lagging_span

# Parabolic SAR
def sar(df, af=0.02, af_max=0.2):
    sar = df['close'].copy()
    ep = df['high'].copy() if df['close'].iloc[1] > df['close'].iloc[0] else df['low'].copy()
    trending_up = df['close'].iloc[1] > df['close'].iloc[0]
    af_value = af

    for i in range(2, len(df)):
        sar.iloc[i] = sar.iloc[i - 1] + af_value * (ep.iloc[i - 1] - sar.iloc[i - 1])

        if trending_up:
            sar.iloc[i] = min(sar.iloc[i], df['low'].iloc[i - 1], df['low'].iloc[i - 2])
            if df['high'].iloc[i] > ep.iloc[i - 1]:
                ep.iloc[i] = df['high'].iloc[i]
                af_value = min(af_value + af, af_max)
            if df['close'].iloc[i] < sar.iloc[i]:
                trending_up = False
                sar.iloc[i] = ep.iloc[i - 1]
                af_value = af
        else:
            sar.iloc[i] = max(sar.iloc[i], df['high'].iloc[i - 1], df['high'].iloc[i - 2])
            if df['low'].iloc[i] < ep.iloc[i - 1]:
                ep.iloc[i] = df['low'].iloc[i]
                af_value = min(af_value + af, af_max)
            if df['close'].iloc[i] > sar.iloc[i]:
                trending_up = True
                sar.iloc[i] = ep.iloc[i - 1]
                af_value = af

    return sar

# Fibonacci Pivot Points
def fib(df):
    PP = (df['high'].shift(1) + df['low'].shift(1) + df['close'].shift(1)) / 3
    R1 = PP + 0.382 * (df['high'].shift(1) - df['low'].shift(1))
    S1 = PP - 0.382 * (df['high'].shift(1) - df['low'].shift(1))
    R2 = PP + 0.618 * (df['high'].shift(1) - df['low'].shift(1))
    S2 = PP - 0.618 * (df['high'].shift(1) - df['low'].shift(1))
    R3 = PP + 1.000 * (df['high'].shift(1) - df['low'].shift(1))
    S3 = PP - 1.000 * (df['high'].shift(1) - df['low'].shift(1))
    return PP, R1, S1, R2, S2, R3, S3
