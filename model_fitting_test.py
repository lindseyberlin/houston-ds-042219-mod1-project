import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
from helpers import *
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.cluster import KMeans
from mpl_toolkits.basemap import Basemap
from sys import maxsize


df = pd.read_csv("kc_house_data.csv")

df["sqft_basement"] = df.apply(replace_null_basement(df), axis=1)
df["date"] = df["date"].apply(lambda x: to_posix(x))
for col in ["yr_renovated", "view", "waterfront"]:
    df[col] = df[col].fillna(0)
df["yr_renovated"] = df["yr_renovated"].apply(lambda x: to_int(x))

KLUSTERS=15
KFOLDS = 4
print('''KLUSTERS=15
KFOLDS = 4''')
print("="*100)

kmeans = KMeans(algorithm="elkan", n_clusters=KLUSTERS).fit(df[["lat", "long"]])
centroids = kmeans.cluster_centers_
df["kcluster_id"] = kmeans.labels_

kclusters = df.groupby("kcluster_id")
k_clusters_tt_splits = []
for i in range(len(kclusters)):
    tt_splits = k_fold_tt_splits(
        KFOLDS,
        kclusters.get_group(i),
    )
    k_clusters_tt_splits.append(tt_splits)

def find_best_model_mse(tt_splits, indep, cols):
    modeling_params = indep+"~"+"+".join(cols)
    best_model = None
    lowest_mse = maxsize
    for data in tt_splits:
        if data[0].shape[0] == 0:
            continue
        model = ols(formula= modeling_params, data=data[0]).fit()
        preds = model.predict(data[1])
        model_mse = rmse_(data[1]["price"], preds)
        if model_mse is None:
            continue
        if model_mse < lowest_mse and model.rsquared > 0:
            lowest_mse = model_mse
            best_model = model
    return best_model, lowest_mse

best_models = []
it = 0
for k_cluster_tt_splits in k_clusters_tt_splits:
    best_model, rmse = find_best_model_mse(k_cluster_tt_splits, "price", ["sqft_living", "grade"])
    if best_model is None:
        continue
    print("rmse: ", rmse, "\n", best_model.summary())
    best_models.append(best_model)