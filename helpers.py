import pandas as pd
import datetime
import time
import re

# to_int: Turns float values into integers
def to_int(x):
    return int(float(x))


# replace_null_basement: Replaces placeholder nulls, in original csv as "?",
# with the value of (sqft_living - sqft_above) as an int
# 
# Usage: df["sqft_basement"] = df.apply(replace_null_basement(df), axis = 1)
def replace_null_basement(df):
    def func(x):
        result = ""
        if x["sqft_basement"] == "?":
            result = x["sqft_living"]-x["sqft_above"]
        else:
            result = x["sqft_basement"]
        return int(float(result))
    return func


# to_posix: Turns strings into UNIX time, assuming the string is formatted as
# month day year and separated by / or -
def to_posix(date):
    dt = datetime.datetime.strptime(date.replace("/", "-"), "%m-%d-%Y")
    posix_dt = time.mktime(dt.timetuple())
    return posix_dt

# 
def df_split(df, n):
    if n == 1:
        return [df]
    result = []
    nr = df.shape[0]
    for i in range(n):
        a = i * nr//n
        b = min(nr, (i+1) * nr//n)
        result.append(df.loc[a:b])
    return result


# k_folds: Creates k-folds
def k_folds(k, A):
    if k == 1:
        yield A
    else:
        for i in range(k-1):
            for f in k_folds(k-1, A):
                yield f
            j = 0
            if (k % 2) == 0:
                j = i
            tmp = A[j]
            A[j] = A[k-1]
            A[k-1] = tmp
        for f in k_folds(k-1, A):
            yield f


# k_fold_tt_splits: Creates k-fold train/test splits
def k_fold_tt_splits(k, df):
    df_splits = df_split(df, k)
    folds = k_folds(k, df_splits)
    tt_splits = []
    for fold in folds:
        joined_df = fold[0].append(fold[1:])
        train = joined_df.iloc[:int(len(joined_df)*4/5)]
        test = joined_df.iloc[int(len(joined_df)/5):]
        tt_splits.append((train, test))
    return tt_splits


# rmse_: Calculates mean squared errors
def rmse_(obsvs, preds):
    if len(obsvs) != len(preds) or len(obsvs) == 0 or len(preds) == 0:
        return None
    obsvs = list(obsvs)
    preds = list(preds)
    result = 0
    for i in range(len(obsvs)):
        result += (obsvs[i]-preds[i])**2
    return (result/len(obsvs))**.5