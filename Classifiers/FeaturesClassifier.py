import pandas
import scipy

# Data =

data = pandas.read_csv("representation_features.csv")

data.corr()["average_rating"]