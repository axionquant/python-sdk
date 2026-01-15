
import numpy as np
import pandas as pd
import parsedatetime
from datetime import datetime, timedelta
from functools import reduce
from tqdm.notebook import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pickle


today = 'today'
now = 'today'
tomorrow = '1 day from now'
yesterday = '1 day ago'
weekago = '1 week ago'
weekfrom = '1 week from today'
monthago = '1 month ago'
monthfrom = '1 month from now'
yearago = '1 year ago'
yearfrom = '1 year from now'
d, day = 'D', 'D'   # daily
w, week = 'W', 'W'  # weekly
m, month = 'M', 'M' # monthly
y, year = 'Y', 'Y'  # annually
h, hour = 'H', 'M'  # hourly

# bool shortcuts
true = True
false = False


# local persistance for method outputs (usually dfs)
def cache(id, fn):
    file_path = f"./.axion_cache/{id}.pkl"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            p = pickle.load(f)
    else:
        p = fn()
        with open(file_path, 'wb') as f:
            pickle.dump(p, f)
    return p

# manually save an item in memory
def save(id, obj):
    file_path = f"./.axion_cache/{id}.pkl"
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)

def read(id):
    file_path = f"./.axion_cache/{id}.pkl"
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            p = pickle.load(f)
            return p

#easily use cache and work functions together
def scribe(df, id, cb):
    data = {}
    def doit():
        work(df, cb, data)
        return data
    return cache(id, lambda: doit())

#natural lang to common date string
def d(date_string):
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(date_string)
    if parse_status == 0:
        # Unable to parse the date string
        return None
    parsed_date = datetime(*time_struct[:6])
    return parsed_date.strftime('%Y-%m-%d')

# if you need a comment for this one, get a grip m8
def to_timestamp(date):
    datetime_obj = datetime.strptime(date, '%Y-%m-%d')
    timestamp = datetime.timestamp(datetime_obj)
    return timestamp

# shortcut to make dataframe
def df(items):
    return pd.DataFrame(items)

# turn 2d list of dicts into 1d list of dataframes (helpful for turning abstract json data to DFs)
def pds(l):
    return [pd.DataFrame(x) for x in l]

# flattens a 2d to 1d in place [[], []] -> [, ,]
def simmer(arr):
    return reduce(lambda a, b: a + b, arr)

def resample(df, dates, col='time'):
    # df[col]=pd.to_datetime(df[col])
    date = dates.split(' ')
    return df[(df[col] > d(date[0])) & (df[col] < d(date[1]))]

# filter out rows by one columns values
def filter(df, col, items):
    return df[df[col].isin(items)]

# get interchange between rows
def relativity(df, cols):
    for c in cols:
        df[f"relative_{c}"] = df[c].pct_change()
    return df.dropna()

# average out a dict of prices to get a comp
def indexed(prices):
    combined_df = pd.concat(prices.values())
    avg_ohlcv_df = combined_df.groupby('time').mean().reset_index()
    return avg_ohlcv_df

# removes duplicate values from list
def dedup(lst):
    return list(set(lst))

# extend multiple dfs of the same style into each other
def stack(dfs):
    return pd.concat(dfs)

# add two different types of data sets together and join on a common col
# quote and econ
def stitch(dfs, col='time'):
    if len(dfs) < 2:
        raise ValueError("At least two DataFrames are required for merging.")

    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=col, how='inner')
    return merged_df

# Combine different instances of the same type of DF
# good for mixing econ sets
def snap(dfs, names=[], overwrite=[], col='time'):
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


def convert_text_to_zero(value):
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


# combine and average out a list of facts or financials
def composite(dfs, joins=['fact', 'label'], col='value'):
    combined_df = pd.concat(dfs)
    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
    average_values = combined_df.groupby(joins)[col].mean().reset_index()
    return average_values

# combine values from multiple facts or fiancial statements into a single indexed df (reshape for graphing)
def contrast(dfs, joins=['CashAndCashEquivalentsAtCarryingValue', 'ShortTermInvestments'], col="fact"):
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
def compare(dfs, joins=['fact','value']):
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



def difference(dfs, col):
    if len(dfs) == 1:
        return dfs[0][~dfs[0][col].isin(set().union(*[df[col] for df in dfs[1:]]))]
    else:
        first_df = dfs[0]
        remaining_dfs = dfs[1:]
        non_overlapping_values = first_df[~first_df[col].isin(set().union(*[df[col] for df in remaining_dfs]))]
        return non_overlapping_values


def overlap(dfs, col):
    if len(dfs) == 1:
        return pd.DataFrame(set(dfs[0][col]), columns=[col])
    else:
        first_df = dfs[0]
        remaining_dfs = dfs[1:]
        overlapping_values = set(first_df[col]).intersection(set(overlap(remaining_dfs, col)[col]))
        return pd.DataFrame(overlapping_values, columns=[col])[col].to_list()



def losers(prices, frame, col='close', relative=True, limit=500):
   return gainers(prices, frame, col, limit, relative=relative, reverse=False)

def gainers(prices, frame, col='close', limit=500, relative=True, reverse=True):
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
def work(df, cb, ref):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(cb, row): row for index, row in df.iterrows()}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Loading Data"):
            try:
                ticker, tdf = future.result()
                ref[ticker] = tdf
            except Exception as e:
                print(f"Error loading data for {ticker}: {e}")


# convert date to a market open one
def nearest_day(date_str, force=False):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    if date.weekday() == 5:
        nearest_trading_day = date - timedelta(days=2)
    elif date.weekday() == 6:
        nearest_trading_day = date + timedelta(days=2)
    else:
        nearest_trading_day = date

    return nearest_trading_day.strftime('%Y-%m-%d')
