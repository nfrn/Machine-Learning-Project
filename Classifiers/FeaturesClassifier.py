import pandas
import scipy

# Data =

# Read in the data
games = pandas.read_csv("representation_features.csv")

# Print the names of the columns in games.
print(games.columns)

# Print the number data points and their size
print(games.shapes)

data.corr()["average_rating"]