import pandas as pd
import datetime
import time


def to_int(x):
    return int(float(x))


def replace_null_basement(df):
    def func(x):
        result = ""
        if x["sqft_basement"] == "?":
            result = x["sqft_living"]-x["sqft_above"]
        else:
            result = x["sqft_basement"]
        return int(float(result))
    return func


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
