import pandas as pd
import numpy as np
from typing import Tuple


def roc(df: pd.DataFrame, column: str = "close", period: int = 10) -> pd.Series:
    """Rate of Change — the percentage change of `column` over `period`."""
    return ((df[column] / df[column].shift(period) - 1) * 100).fillna(0)


def mom(df: pd.DataFrame, column: str = "close", period: int = 10) -> pd.Series:
    """Momentum — the absolute difference of `column` over `period` periods."""
    return df[column].diff(period)


def sma(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Simple Moving Average — the mean of `column` over `period`."""
    return df[column].rolling(window=period, min_periods=1).mean()


def smm(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Simple Moving Median — the median of `column` over `period`."""
    return df[column].rolling(window=period).median()


def ssma(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Smoothed Simple Moving Average — an EMA of the SMA with alpha = 1/period."""
    initial_sma = df[column].rolling(window=period).mean()
    return initial_sma.ewm(alpha=1 / period, adjust=False).mean()


def ema(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Exponential Moving Average — weighted mean with span `period`."""
    return df[column].ewm(span=period, adjust=False).mean()


def dema(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Double Exponential Moving Average — 2*EMA - EMA(EMA) to reduce lag."""
    ema = df[column].ewm(span=period, adjust=False).mean()
    return 2 * ema - ema.ewm(span=period, adjust=False).mean()


def trima(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Triangular Moving Average — a double-smoothed SMA (SMA of SMA)."""
    sma = df[column].rolling(window=period).mean()
    return sma.rolling(window=period).mean()


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average True Range — the mean of the true range over `period`."""
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def stochastic_oscillator(
    df: pd.DataFrame, k_period: int = 14, d_period: int = 3
) -> Tuple[pd.Series, pd.Series]:
    """Stochastic Oscillator — %K and %D lines indicating overbought/oversold levels."""
    low_min = df['low'].rolling(window=k_period).min()
    high_max = df['high'].rolling(window=k_period).max()
    K = ((df['close'] - low_min) / (high_max - low_min)) * 100
    D = K.rolling(window=d_period).mean()
    return K, D


def cmo(df: pd.DataFrame, column: str = "close", period: int = 20) -> pd.Series:
    """Chande Momentum Oscillator — momentum-based oscillator ranging from -100 to +100."""
    delta = df[column].diff(1)
    up = delta.where(delta > 0, 0).rolling(window=period).sum()
    down = -delta.where(delta < 0, 0).rolling(window=period).sum()
    return ((up - down) / (up + down)) * 100


def obv(df: pd.DataFrame) -> pd.Series:
    """On-Balance Volume — cumulative volume adjusted by price direction."""
    return (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()


def vpt(df: pd.DataFrame) -> pd.Series:
    """Volume-Price Trend — cumulative product of volume and percentage price change."""
    return (
        df['volume']
        * ((df['close'] - df['close'].shift(1)) / df['close'].shift(1))
    ).cumsum()


def vwap(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Volume-Weighted Average Price — cumulative VWAP using typical price."""
    return (
        (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum()
        / df['volume'].cumsum()
    )


def bbands(
    df: pd.DataFrame, column: str = "close", period: int = 20, num_std_dev: int = 2
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Bollinger Bands — upper band, SMA, and lower band around price."""
    sma = df[column].rolling(window=period).mean()
    std_dev = df[column].rolling(window=period).std()
    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)
    return upper_band, sma, lower_band


def kc(
    df: pd.DataFrame, period: int = 20, atr_period: int = 10, multiplier: float = 2
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Keltner Channels — SMA with ATR-based upper and lower bands."""
    sma = df['close'].rolling(window=period).mean()
    atr_val = atr(df, period=atr_period)
    upper_channel = sma + (atr_val * multiplier)
    lower_channel = sma - (atr_val * multiplier)
    return upper_channel, sma, lower_channel


def kama(
    df: pd.DataFrame,
    column: str = "close",
    period: int = 14,
    fast: int = 14,
    slow: int = 30,
) -> pd.Series:
    """Kaufman Adaptive Moving Average — adjusts sensitivity based on market noise."""
    df['direction'] = df[column] - df[column].shift(period)
    df['volatility'] = df[column].diff().abs().rolling(window=period).sum()
    df['ER'] = df['direction'] / df['volatility']
    sc = (
        (df['ER'] * (2 / (fast + 1) - 2 / (slow + 1)) + 2 / (slow + 1)) ** 2
    ).fillna(0)
    kama = [df[column].iloc[0]]
    for i in range(1, len(df)):
        kama.append(kama[-1] + sc.iloc[i] * (df[column].iloc[i] - kama[-1]))
    return pd.Series(kama, index=df.index)


def vi(
    df: pd.DataFrame, period: int = 14
) -> Tuple[pd.Series, pd.Series]:
    """Vortex Indicator — VI+ and VI- measuring trend direction and strength."""
    TR = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1)),
        ),
    )
    TR_sum = TR.rolling(window=period).sum()
    VM_plus = abs(df['high'] - df['low'].shift(1))
    VM_minus = abs(df['low'] - df['high'].shift(1))
    VI_plus = VM_plus.rolling(window=period).sum() / TR_sum
    VI_minus = VM_minus.rolling(window=period).sum() / TR_sum
    return VI_plus, VI_minus


def macd(
    df: pd.DataFrame,
    column: str = "close",
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """MACD — moving average convergence/divergence: line, signal, and histogram."""
    ema_fast = df[column].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow_period, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Williams %R — overbought/oversold oscillator ranging from -100 to 0."""
    high_max = df['high'].rolling(window=period).max()
    low_min = df['low'].rolling(window=period).min()
    return -100 * (high_max - df['close']) / (high_max - low_min)


def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Average Directional Index — trend strength indicator from smoothed DX."""
    tr = atr(df, period=1)
    plus_dm = df['high'].diff()
    minus_dm = df['low'].diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    plus_dm_smooth = plus_dm.rolling(window=period).sum()
    minus_dm_smooth = abs(minus_dm.rolling(window=period).sum())
    plus_di = 100 * (plus_dm_smooth / tr)
    minus_di = 100 * (minus_dm_smooth / tr)
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    return dx.rolling(window=period).mean()


def rsi(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Relative Strength Index — momentum oscillator ranging from 0 to 100."""
    delta = df[column].diff(1)
    gain = delta.where(delta > 0, 0).fillna(0)
    loss = -delta.where(delta < 0, 0).fillna(0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def ichi(
    df: pd.DataFrame,
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """Ichimoku Cloud — conversion, base, leading spans A/B, and lagging span."""
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


def sar(df: pd.DataFrame, af: float = 0.02, af_max: float = 0.2) -> pd.Series:
    """Parabolic SAR — trailing stop-and-reversal indicator."""
    sar = df['close'].copy()
    ep = (
        df['high'].copy()
        if df['close'].iloc[1] > df['close'].iloc[0]
        else df['low'].copy()
    )
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


def fib(
    df: pd.DataFrame,
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """Fibonacci Pivot Points — pivot, 3 resistance, and 3 support levels."""
    PP = (df['high'].shift(1) + df['low'].shift(1) + df['close'].shift(1)) / 3
    R1 = PP + 0.382 * (df['high'].shift(1) - df['low'].shift(1))
    S1 = PP - 0.382 * (df['high'].shift(1) - df['low'].shift(1))
    R2 = PP + 0.618 * (df['high'].shift(1) - df['low'].shift(1))
    S2 = PP - 0.618 * (df['high'].shift(1) - df['low'].shift(1))
    R3 = PP + 1.000 * (df['high'].shift(1) - df['low'].shift(1))
    S3 = PP - 1.000 * (df['high'].shift(1) - df['low'].shift(1))
    return PP, R1, S1, R2, S2, R3, S3
