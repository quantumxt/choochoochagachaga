# Data analysis libraries
import pandas as pd
import numpy as np

# Machine learning libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Database libraries
from cloudant.client import Cloudant
from cloudant.query import Query

client = Cloudant.iam("adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix", "4aQghGIAIrBzsJRx2fbspghgtQXPWLTfmvZKpetOaO7K", connect=True)
client.connect()

# Obtain database
smart_env = client['smart_environment']
query = Query(smart_env, selector={'_id': {'$gt': 0}})
receive = pd.DataFrame(query()['docs']).drop(['_id', '_rev'], axis=1)

# Heart Rate
def query_heart(embedded_data):
    return embedded_data['bpm'].tolist()

# Temp
def query_temp(embedded_data):
    return embedded_data['temperature'].tolist()

# Altitude
def query_altitude(embedded_data):
    return embedded_data['altitude'].tolist()

# Location
def query_location(embedded_data):
    return embedded_data['location'].tolist()

# mission = pd.DataFrame(pd.DataFrame(pd.DataFrame(receive['info']).iloc[0].iloc[0]).iloc[0][0]) # BATCH_NUMBER | TEAM_NUMBER | MEMBER
# print(mission.head())
print("Altitude", query_altitude(mission))
print()
print("Heart", query_heart(mission))
print()
print("Location", query_location(mission))
print()
print("Temperature", query_temp(mission))

def to_df_format(input):
    '''Transform data from mongodb to machine learning format'''
    pass

X_train, y_train = to_df_format(mission)
regressor = RandomForestRegressor(n_estimators=30, random_state=42)
regressor.fit(X_train, y_train)

def get_current_stats():
    ''' Obtain the current details about the environment and trainee profile
    so that we get predictions on it'''
    pass

current_stats = get_current_stats()
prediction = regressor.predict(current_stats)