"""Train bikes model."""
import numpy as np
import pandas as pd
import pickle as pkl

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from sklearn.pipeline import Pipeline

np.random.seed(0)

df = pd.read_csv('data/day.csv', index_col=0)

X_values = df.loc[:,('season',
                     'yr',
                     'mnth',
                     'holiday',
                     'weekday',
                     'workingday',
                     'weathersit',
                     'temp',
                     'atemp',
                     'hum',
                     'windspeed',
                     'cnt'
                     )]

X_values.rename(columns={
    'yr': 'year',
    'mnth': 'month',
    'weekday': 'week_day',
    'workingday': 'working_day',
    'weathersit': 'weather',
    'temp': 'temperature',
    'atemp': 'feeling_temperature',
    'hum': 'humidity',
    'windspeed': 'wind_speed',
    'cnt': 'y'
    }, inplace=True)

y_values = X_values.pop("y")

X_train, X_test, y_train, y_test = train_test_split(
    X_values, y_values, test_size=0.40)
cols = X_train.columns
# Save data before transformations
X_train['y'] = y_train
X_test['y'] = y_test
X_train.to_csv('bikes_train.csv')
X_test.to_csv('bikes_test.csv')
X_train.pop("y")
X_test.pop("y")

X_train = X_train.values
X_test = X_test.values

# Setup pipeline
lr_pipeline = Pipeline([
    ('lr', LinearRegression())
    ])
lr_pipeline.fit(X_train, y_train)

print("Train Score:", lr_pipeline.score(X_train, y_train))
print("Score:", lr_pipeline.score(X_test, y_test))
print("Portion y==0:", np.sum(y_test.values == 0)
      * 1. / y_test.values.shape[0])

print("Column names: ", cols)
# print("Coefficients: ", lr_pipeline.named_steps["lr"].coef_)

with open("bikes_model_linear_regression.pkl", "wb") as f:
    pkl.dump(lr_pipeline, f)

print("Saved model!")
