from nba_api.stats.endpoints import commonallplayers, playercareerstats
import json
from sklearn import linear_model
import pandas as pd
import time
from matplotlib import pyplot as plt

#df_data = pd.DataFrame()

df_data = pd.read_csv("TrainingData.csv")
targetPTS = df_data.drop(['Unnamed: 0', 'PLAYER_ID',  'GP',   'MIN', 
 'FGM',  'FG_PCT',  'FG3M',  'FG3_PCT',  'FTM',  'FT_PCT',   'REB',  'AST',  'STL',  'BLK'], axis=1)
df_data = df_data.drop(['PTS', 'Unnamed: 0', 'PLAYER_ID','GP', 'MIN', 'FG3_PCT'
, 'BLK', 'STL', 'REB', 'AST', 'FG3M', 'FT_PCT', 'FG_PCT'], axis=1)


df_testdata = pd.read_csv("rookieTestData.csv")
testPTS = df_testdata.drop(['Unnamed: 0', 'PLAYER_ID',  'GP',   'MIN', 
 'FGM',  'FG_PCT',  'FG3M',  'FG3_PCT',  'FTM',  'FT_PCT',   'REB',  'AST',  'STL',  'BLK'], axis=1)
df_testdata = df_testdata.drop(['PTS', 'Unnamed: 0', 'PLAYER_ID','GP', 'MIN', 'FG3_PCT'
, 'BLK', 'STL', 'REB', 'AST', 'FG3M', 'FT_PCT', 'FG_PCT'], axis=1)

print(df_testdata)
print(testPTS)


df_data = df_data.fillna(0)

X = df_data
y = targetPTS

Xa = df_testdata
ya = testPTS

#print(X)
#print(y)

lm = linear_model.LinearRegression()
model = lm.fit(X, y)

predictions = lm.predict(Xa)
print(predictions)
#print(lm.score(X,y))


plt.scatter(ya, predictions)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.show()