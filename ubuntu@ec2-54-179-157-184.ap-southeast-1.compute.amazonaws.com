#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import json

# Data analysis libraries
import pandas as pd
import numpy as np

# Machine learning libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Database libraries
from cloudant.client import Cloudant
from cloudant.query import Query

@app.route('/batch_stats', methods=['GET'])
def get_batch_stats()
    batch_no = request.args.get("batch")
    client = Cloudant.iam("adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix", "4aQghGIAIrBzsJRx2fbspghgtQXPWLTfmvZKpetOaO7K", connect=True)
    client.connect()

    # Obtain database
    smart_env = client['smart_environment']
    query = Query(smart_env, selector={'_id': {'batch': batch_no}})
    receive = pd.DataFrame(query()['docs']).drop(['_id', '_rev'], axis=1)
    # Helper Functions

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

    def query_details(batch,team,member):
        mission = pd.DataFrame(pd.DataFrame(pd.DataFrame(receive['info']).iloc[batch].iloc[team]).iloc[member])
        rows = len(mission.index)
        data = {}
        for i in range(rows):
            jsonstr = pd.DataFrame(mission.iloc[i])[i].to_json()
            d = json.loads(jsonstr)["1"]
            data[i] = d
        return pd.DataFrame.from_dict(data, orient='index')

    mission = query_details(0,0,1)
    print(mission.head())
    #print("Altitude", query_altitude(mission))
    print()
    #print("Heart", query_heart(mission))
    print()
    #print("Location", query_location(mission))
    print()
    #print("Temperature", query_temp(mission))

    def get_bpm_spike(mission):
        data = []
        for i in range(len(mission.index) - 1):
            bpm1 = mission.loc[i,"bpm"]
            bpm2 = mission.loc[i+1,"bpm"]
            if (bpm2 - bpm1) > 50:
                data.append((bpm1,bpm2,mission.loc[i,"time"]))
        return data
    get_bpm_spike(mission)


    stats = mission.describe()

    start = stats.loc["min","time"]
    end = stats.loc["max","time"] 


    time_taken = (end - start)/(60)

    bpm_spikes =  get_bpm_spike(mission)
    spikes = []
    for i in range(len(bpm_spikes)):
        spike_point = [end - bpm_spikes[i][2], bpm_spikes[i][0], bpm_spikes[i][1]]
        spikes.append(spike_point)


    to_save = {"Trainee": mission.loc[0,"names"], "MissionTime": time_taken, 
               "BPM": int(stats.loc["mean","bpm"]), "Temp": int(stats.loc["mean","temperature"]),
               "AltMax": stats.loc["max","altitude"], "AltMin": stats.loc["min","altitude"].
               "SpikesBPM": spikes}

    return send_file(json.dump(to_save))

app.run(host="ec2-54-179-157-184.ap-southeast-1.compute.amazonaws.com", port=8082, debug=False)