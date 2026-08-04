
import numpy as np
import pandas as pd
import parsedatetime
from datetime import datetime, timedelta
from functools import reduce
from tqdm.notebook import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pickle
from typing import Any, Optional, Callable


D, day = 'D', 'D'   # daily
W, week = 'W', 'W'  # weekly
Q, quarter = 'Q', 'Q'  # quarterly
M, month = 'M', 'M' # monthly
Y, year = 'Y', 'Y'  # annually

# bool shortcuts
true = True
false = False


# local persistance for method outputs (usually dfs)
def cache(id: str, fn: Callable):
    """Load cached result from disk or compute and cache it."""
    file_path = f"./.axion_cache/{id}.pkl"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            p = pickle.load(f)
    else:
        p = fn()
        os.makedirs("./.axion_cache", exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(p, f)
    return p

# manually save an item in memory
def save(id: str, obj: Any) -> None:
    """Serialize and persist an object to disk cache."""
    file_path = f"./.axion_cache/{id}.pkl"
    os.makedirs("./.axion_cache", exist_ok=True)
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def read(id: str) -> Optional[Any]:
    """Deserialize and return a cached object from disk, or None."""
    file_path = f"./.axion_cache/{id}.pkl"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            p = pickle.load(f)
            return p

#easily use cache and work functions together
def scribe(df: pd.DataFrame, id: str, cb: Callable) -> dict:
    """Cache the result of work() applied to a DataFrame."""
    data = {}
    def doit():
        work(df, cb, data)
        return data
    return cache(id, lambda: doit())

#natural lang to common date string
def d(date_string: str) -> Optional[str]:
    """Convert a natural language date string to '%Y-%m-%d' format."""
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(date_string)
    if parse_status == 0:
        # Unable to parse the date string
        return None
    parsed_date = datetime(*time_struct[:6])
    return parsed_date.strftime('%Y-%m-%d')

#natural lang to common date string
def date(date_string: str) -> Optional[str]:
    return d(date_string)

# if you need a comment for this one, get a grip m8
def to_timestamp(date: str) -> float:
    """Convert a '%Y-%m-%d' date string to a Unix timestamp."""
    datetime_obj = datetime.strptime(date, '%Y-%m-%d')
    timestamp = datetime.timestamp(datetime_obj)
    return timestamp

# shortcut to make dataframe
def df(items: Any) -> pd.DataFrame:
    """Create a DataFrame from the given data."""
    return pd.DataFrame(items)

#resize frame based on start and end dates
def ranger(df: pd.DataFrame, start: str, end: str = None, date_col: str = "date") -> pd.DataFrame:
    """Filter a DataFrame to rows within a date range [start, end]."""
    if date_col not in df.columns:
        raise ValueError(f"Column '{date_col}' not found")

    target = df.copy()

    # normalize to datetime with UTC
    target[date_col] = pd.to_datetime(target[date_col], utc=True)

    start = pd.to_datetime(start, utc=True)
    end = pd.to_datetime(end, utc=True) if end else None

    if end is not None:
        mask = (target[date_col] >= start) & (target[date_col] <= end)
    else:
        mask = target[date_col] >= start

    return target.loc[mask]


# turn 2d list of dicts into 1d list of dataframes (helpful for turning abstract json data to DFs)
def pds(l: list) -> list:
    """Convert each sublist of dicts into a DataFrame."""
    return [pd.DataFrame(x) for x in l]

# flattens a 2d to 1d in place [[], []] -> [, ,]
def simmer(arr: list) -> list:
    """Flatten a 2D list into a 1D list."""
    return reduce(lambda a, b: a + b, arr)

def resample(df: pd.DataFrame, dates: str, col: str = 'time') -> pd.DataFrame:
    """Filter a DataFrame to rows between two natural-language dates."""
    date = dates.split(' ')
    return df[(df[col] > d(date[0])) & (df[col] < d(date[1]))]

# filter out rows by one columns values
def filter(df: pd.DataFrame, col: str, items: list) -> pd.DataFrame:
    """Filter rows where the column value is in items."""
    return df[df[col].isin(items)]

# get interchange between rows
def relativity(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Add percentage-change columns for each specified column."""
    for c in cols:
        df[f"relative_{c}"] = df[c].pct_change()
    return df.dropna()

# average out a dict of prices to get a comp
def indexed(prices: dict) -> pd.DataFrame:
    """Average OHLCV data across multiple price DataFrames."""
    combined_df = pd.concat(prices.values())
    avg_ohlcv_df = combined_df.groupby('time').mean().reset_index()
    return avg_ohlcv_df

# removes duplicate values from list
def dedup(lst: list) -> list:
    """Remove duplicate values from a list while preserving no order."""
    return list(set(lst))

# extend multiple dfs of the same style into each other
def stack(dfs: list) -> pd.DataFrame:
    """Vertically concatenate multiple DataFrames."""
    return pd.concat(dfs)

# add two different types of data sets together and join on a common col
# quote and econ
def stitch(dfs: list, col: str = 'time') -> pd.DataFrame:
    """Merge multiple DataFrames on a common column using inner joins."""
    if len(dfs) < 2:
        raise ValueError("At least two DataFrames are required for merging.")

    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=col, how='inner')
    return merged_df

# Combine different instances of the same type of DF
# good for mixing econ sets
def snap(dfs: list, names: list = [], overwrite: list = [], col: str = 'time') -> pd.DataFrame:
    """Merge DataFrames on a time column and rename overlapping columns."""
    tr = [col]
    for df in dfs:
        df[col] = pd.to_datetime(df[col])

    merged_df = dfs[0]

    for i, df in enumerate(dfs[1:], start=1):
        current_suffixes = ('', f'_df{i}')
        merged_df = pd.merge(merged_df, df, on=col, suffixes=current_suffixes)

    for y, v in enumerate(overwrite):
        for i, name in enumerate(names):
            original_col_name = v if i == 0 else f"{v}_df{i}"
            if original_col_name in merged_df.columns:
                new_col_name = name if y == 0 else f"{name}_{v}"
                tr.append(new_col_name)
                merged_df[new_col_name] = merged_df[original_col_name]
                merged_df = merged_df.drop(columns=[original_col_name])
    return merged_df[tr]


def convert_text_to_zero(value: Any) -> float:
    """Convert string values to float, returning 0 for non-numeric or missing."""
    if isinstance(value, str):
        try:
            float_value = float(value)
            if np.isnan(float_value) or value == 'None' or value is None:
                return 0
            else:
                return float_value
        except ValueError:
            return 0
    else:
        return value

# Convert two adjacent lists into a single dict
# good for combining a list of tickers with the values loaded from a looped operation
def zap(labels: list, values: list) -> dict:
    return dict(zip(labels, values))

# combine and average out a list of facts or financials
def composite(dfs: list, joins: list = ['fact', 'label'], col: str = 'value') -> pd.DataFrame:
    """Average values across multiple DataFrames grouped by key columns."""
    combined_df = pd.concat(dfs)
    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
    average_values = combined_df.groupby(joins)[col].mean().reset_index()
    return average_values

# combine values from multiple facts or fiancial statements into a single indexed df (reshape for graphing)
def contrast(dfs: list, joins: list = ['CashAndCashEquivalentsAtCarryingValue', 'ShortTermInvestments'], col: str = "fact") -> pd.DataFrame:
    """Reshape financial-fact DataFrames into a single indexed DataFrame."""
    cdf = None
    for df in dfs:
        ap = {}
        ap['date'] = get_value(df, 'time', col=col)
        for j in joins:
            ap[j] = get_value(df, j, col=col)

        if cdf is None:
            cdf = pd.DataFrame([ap])
        else:
            cdf = pd.concat([cdf, pd.DataFrame([ap])], ignore_index=True)

    return cdf

# show interchange between columns with the same name across multiple dfs
def compare(dfs: list, joins: list = ['fact', 'value']) -> pd.DataFrame:
    """Compute percentage differences between matching columns across DataFrames."""
    if not dfs or len(dfs) < 2:
        raise ValueError("At least two DataFrames are required for comparison.")

    df_merged = dfs[0][dfs[0].columns].copy()

    for i, df in enumerate(dfs[1:], start=1):
        df_to_merge = df[joins].copy()
        for y, x in enumerate(joins[1:], start=1):
            df_to_merge.rename(columns={x: f'{x}_{i}'}, inplace=True)

        df_merged = pd.merge(df_merged, df_to_merge, on=joins[0], how='left', suffixes=('', f'_{i}'))

    for i in range(1, len(dfs)):
        for y, x in enumerate(joins[1:], start=1):
            value_col_first = x if i == 1 else f'{x}_{i-1}'
            value_col_next = f'{x}_{i}'

            df_merged[value_col_first] = pd.to_numeric(df_merged[value_col_first], errors='coerce').fillna(0)
            df_merged[value_col_next] = pd.to_numeric(df_merged[value_col_next], errors='coerce').fillna(0)

            pct_diff_col_name = f'{x}_pct_diff_{i}'
            df_merged[pct_diff_col_name] = (( df_merged[value_col_first] - (df_merged[value_col_next]) ) / df_merged[value_col_first].replace({0: pd.NA})) * 100

    return df_merged



def difference(dfs: list, col: str) -> pd.DataFrame:
    """Return rows from the first DataFrame whose column value is absent in the rest."""
    if len(dfs) == 1:
        return dfs[0][~dfs[0][col].isin(set().union(*[df[col] for df in dfs[1:]]))]
    else:
        first_df = dfs[0]
        remaining_dfs = dfs[1:]
        non_overlapping_values = first_df[~first_df[col].isin(set().union(*[df[col] for df in remaining_dfs]))]
        return non_overlapping_values


def overlap(dfs: list, col: str) -> Any:
    """Return column values present across all DataFrames."""
    if len(dfs) == 1:
        return pd.DataFrame(set(dfs[0][col]), columns=[col])
    else:
        first_df = dfs[0]
        remaining_dfs = dfs[1:]
        overlapping_values = set(first_df[col]).intersection(set(overlap(remaining_dfs, col)[col]))
        return pd.DataFrame(overlapping_values, columns=[col])[col].to_list()



def losers(prices: dict, frame: int, col: str = 'close', relative: bool = True, limit: int = 500) -> pd.DataFrame:
    """Return top losers by price change over a lookback window."""
    return gainers(prices, frame, col, limit, relative=relative, reverse=False)

def gainers(prices: dict, frame: int, col: str = 'close', limit: int = 500, relative: bool = True, reverse: bool = True) -> pd.DataFrame:
    """Return top gainers (or losers) by price change over a lookback window."""
    top_gainers = {}
    for ticker, df in prices.items():
        if len(df) > frame:
            if relative:
                gain = ((df[col].iloc[-1] - df[col].iloc[-frame])/df[col].iloc[-1])*100
            else:
                gain = df[col].iloc[-1] - df[col].iloc[-frame]
            top_gainers[ticker] = gain
    return pd.DataFrame(sorted(top_gainers.items(), key=lambda x: x[1], reverse=reverse)[:limit], columns=["ticker","change"])


# easy concurency function
def work(df: pd.DataFrame, cb: Callable, ref: dict) -> None:
    """Apply a callback concurrently to each row of a DataFrame."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(cb, row): row for index, row in df.iterrows()}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Loading Data"):
            try:
                ticker, tdf = future.result()
                ref[ticker] = tdf
            except Exception as e:
                print(f"Error loading data for {ticker}: {e}")


# convert date to a market open one
def nearest_day(date_str: str, force: bool = False) -> str:
    """Shift a date to the nearest weekday (trading day)."""
    date = datetime.strptime(date_str, '%Y-%m-%d')
    if date.weekday() == 5:
        nearest_trading_day = date - timedelta(days=2)
    elif date.weekday() == 6:
        nearest_trading_day = date + timedelta(days=2)
    else:
        nearest_trading_day = date

    return nearest_trading_day.strftime('%Y-%m-%d')
