import pandas as pd
import datetime
import time


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


# def k_folds(n, A):
#     print(n, A)
#     if n == 1:
#         return A
#     else:
#         result = []
#         for i in range(n-1):
#             for f in k_folds(n-1, A):
#             j = 0
#             if (n % 2) == 0:
#                 j = i
#             tmp = A[j]
#             A[j] = A[n-1]
#             A[n-1] = tmp


def k_folds(n, A):
    # print(n, A)
    if n == 1:
        yield A
    else:
        for i in range(n-1):
            for f in k_folds(n-1, A):
                yield f
            j = 0
            if (n % 2) == 0:
                j = i
            tmp = A[j]
            A[j] = A[n-1]
            A[n-1] = tmp
        for f in k_folds(n-1, A):
            yield f