import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

dataset = pd.read_csv('features_45k.csv')
dfy = pd.DataFrame(dataset["popularity"])
dfx = dataset.drop(columns=['Artist', 'Track','popularity'])

dfy['popularity'].fillna(0, inplace=True)

dfx['followers', 'instrumentalness', 'acousticness', 'danceability', 'duration_ms', 'energy', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence'].fillna(dataset['followers', 'instrumentalness', 'acousticness', 'danceability', 'duration_ms', 'energy', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence'].mean(), inplace=True)

X = dfx
y = dfy
#trying to get rid of >ValueError: Input contains NaN, infinity or a value too large for dtype('float64').
np.where(dfx.values >= np.finfo(np.float64).max)
np.isnan(dfx.values.any())
dfx.replace([np.inf, -np.inf], np.nan, inplace=True)

#trying to get rid of >ValueError: Input contains NaN, infinity or a value too large for dtype('float64').
np.where(dfy.values >= np.finfo(np.float64).max)
np.isnan(dfy.values.any())
dfy.replace([np.inf, -np.inf], np.nan, inplace=True)

dfx.reset_index(inplace=True, drop=True)
dfy.reset_index(inplace=True, drop=True)

def convert_to_int(word):
    word_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8,
                'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'zero':0, 0: 0}
    return word_dict[word]


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
# model
X_train, X_test, y_train, y_test = train_test_split(dfx, dfy, test_size=0.3, random_state=42)
# linear regression
LR_model = LinearRegression()
LR_model.fit(X_train, y_train)



pickle.dump(LR_model, open('Pickle_LR_Model.pkl','wb'))

model = pickle.load(open('Pickle_LR_Model.pkl','rb'))
print(model.predict([['Tonight Will Be Alright','Lionel Richie']]))