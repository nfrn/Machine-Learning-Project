import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
from scipy.stats import spearmanr, pearsonr
import time
from sklearn import metrics

from sklearn.multioutput import MultiOutputRegressor


# Data =
if __name__ == "__main__":
    games = pd.read_csv("generated_weights.csv", header=None, delimiter=",")
    # rows,"cols","time_limit","nb_chain_weight","avg_chain_weight","max_chain_weight","winrate","drawrate"
    train = games.sample(frac=0.9, random_state=1)
    test = games.loc[~games.index.isin(train.index)]

    print(train.shape)
    print(test.shape)


    columns = games.columns.tolist()
    print(columns)
    columns_1 = [c for c in columns if c not in [3,4,5,6,7]]
    target = [3,4,5,6]


    model1 = MultiOutputRegressor(
        RandomForestRegressor(n_estimators=1000, bootstrap=True, max_depth=100, min_samples_leaf=4, min_samples_split=5, n_jobs=4))

    model1.fit(train[columns_1], train[target])

    start = time.time()
    predictions = model1.predict(test[columns_1])
    end = time.time()

    test_score = r2_score(test[target], predictions)
    spearman = spearmanr(test[target], predictions)


    mean_square = mean_squared_error(predictions, test[target])

    print(f'Test mean square erro: {mean_square:.3}')
    print(f'Test data R-2 score: {test_score:>5.3}')
    print("Time:" + str(end - start))