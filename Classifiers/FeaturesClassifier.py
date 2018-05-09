import pandas
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



# Data =
if __name__ == "__main__":
    games = pandas.read_csv("stateToFeatures2.csv", header=None, delimiter=",")

    train = games.sample(frac=0.8, random_state=1)
    test = games.loc[~games.index.isin(train.index)]

    print(train.shape)
    print(test.shape)

    columns = games.columns.tolist()


    columns_1 = [c for c in columns if c not in [3,4]]

    # Store the variable we'll be predicting on.
    target = 4

    #model = LinearRegression()
    model1 = RandomForestRegressor(n_estimators=400, min_samples_leaf=2, random_state=1)
    #model = SVR()

    model1.fit(train[columns_1], train[target])
    predictions = model1.predict(test[columns_1])
    # model1.in
    print(test[columns_1].shape)
    print(mean_squared_error(predictions, test[target]))
    filename = 'features_classifier_1.sav'
    joblib.dump(model1, filename)

    columns_1 = [c for c in columns if c not in [3]]

    # Store the variable we'll be predicting on.
    target = 3

    #model2 = LinearRegression()
    model2 = RandomForestRegressor(n_estimators=400, min_samples_leaf=2, random_state=1)
    #model2 = SVR()

    model2.fit(train[columns_1], train[target])
    predictions = model2.predict(test[columns_1])
    print(test[columns_1].shape)
    print(mean_squared_error(predictions, test[target]))
    filename = 'features_classifier_2.sav'
    joblib.dump(model2, filename)


