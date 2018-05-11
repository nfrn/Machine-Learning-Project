import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import time


# Data =
if __name__ == "__main__":
    games = pd.read_csv("stateToFeatures2.csv", header=None, delimiter=",")

    train = games.sample(frac=0.8, random_state=1)
    test = games.loc[~games.index.isin(train.index)]


    print(train.shape)
    print(test.shape)

    columns = games.columns.tolist()
    columns_1 = [c for c in columns if c not in [3,4,5]]
    target = [3,4,5]

    scaler = StandardScaler().fit(train[columns_1])
    X_train_scaled = pd.DataFrame(scaler.transform(train[columns_1]),
                                  index=train[columns_1].index.values,
                                  columns=train[columns_1].columns.values)
    X_test_scaled = pd.DataFrame(scaler.transform(test[columns_1]),
                                 index=test[columns_1].index.values,
                                 columns=test[columns_1].columns.values)


    model1 = RandomForestRegressor(n_estimators=10,bootstrap=True,
                                   max_depth=40,min_samples_leaf=4,
                                   min_samples_split=5)

    model1.fit(train[columns_1], train[target])

    start = time.time()
    predictions = model1.predict(test[columns_1])
    end = time.time()

    test_score = r2_score(test[target], predictions)


    mean_square = mean_squared_error(predictions, test[target])

    print(f'Test mean square erro: {mean_square:.3}')
    print(f'Test data R-2 score: {test_score:>5.3}')
    print("Time:" + str(end - start))
    filename = 'total.sav'
    joblib.dump(model1, filename)
