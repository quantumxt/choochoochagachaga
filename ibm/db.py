from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import time
import numpy as np

# Replicator source
# {
#   "apikey": "o7S3eUhKalxAUYQx3sGeMb1xKwQTYZGpetNu0DgRfhg9",
#   "host": "adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix.cloudantnosqldb.appdomain.cloud",
#   "iam_apikey_description": "Auto-generated for key baa3716d-88a1-4412-abca-f36dbc03cb92",
#   "iam_apikey_name": "replicator-source",
#   "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/fdfb95665c2f499e8b0534ff52bf59f1::serviceid:ServiceId-4dee03bf-edc3-4c73-9938-4a1d7273b92c",
#   "url": "https://adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix.cloudantnosqldb.appdomain.cloud",
#   "username": "adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix"
# }

# Replicator target
# {
#   "apikey": "STW7guruqQZYg0xjlxTufA4uaf0-Go8g7SQz8B7Oe0xQ",
#   "host": "adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix.cloudantnosqldb.appdomain.cloud",
#   "iam_apikey_description": "Auto-generated for key 5d17ffce-83c0-4610-b443-16c9674d4610",
#   "iam_apikey_name": "replicator-target",
#   "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/fdfb95665c2f499e8b0534ff52bf59f1::serviceid:ServiceId-75e178ea-cb41-4989-bbb0-8db8f2770b02",
#   "url": "https://adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix.cloudantnosqldb.appdomain.cloud",
#   "username": "adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix"
# }

# API key access
# {
#   "apikey": "zQRIu-XTG6EgQJRibXzJmkOUUwW-zVd-tCEEjGdmoh8H",
#   "host": "adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix.cloudantnosqldb.appdomain.cloud",
#   "iam_apikey_description": "Auto-generated for key 5e60bfd9-70ed-4d58-b917-943fe0aa70e8",
#   "iam_apikey_name": "Service credentials-1",
#   "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/fdfb95665c2f499e8b0534ff52bf59f1::serviceid:ServiceId-cdc24205-735e-442d-9428-7064641203d2",
#   "url": "https://adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix.cloudantnosqldb.appdomain.cloud",
#   "username": "adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix"
# }

"""
1) Heart Rate
2) Temperature
3) Altitude
4) Location (X,Y)
"""
NAMES = ["john", 'doe', 'ah teck', 'lim choo min', 'jacelyn teo', 'goel lalit', 'samuel', 'chewy baca']
client = Cloudant.iam("adef00a8-b0a0-4d14-8305-6be0563ed542-bluemix", "zQRIu-XTG6EgQJRibXzJmkOUUwW-zVd-tCEEjGdmoh8H")
client.connect()

db_name = "smart_environment"
env_database = client.create_database(db_name)

if env_database.exists():
   print(f"'{db_name}' successfully created.")

sample_data = []
for i in range(np.random.randint(20)): # Person
    batch_data = []
    name = NAMES[np.random.randint(7)] + str(round(np.random.randn(), 3))
    for j in range(500): #Training 
        var = {"names": name, 
               "time": int(time.time()), 
               "bpm": np.random.randint(60, 120), 
               "temperature": np.random.randint(20, 60), 
               "altitude": np.random.randint(-10, 300), 
               "location": [np.random.rand(), np.random.randn()]}
        batch_data.append(var)    
    sample_data.append(batch_data)

# {"basic_info": [{"name": , "age": , "height": , "weight": , "load": , "specs": , "exp": , "qual": , "ippt": }, 
# {"name": , "age": , "height": , "weight": , "load": , "specs": , "exp": , "qual": , "ippt": }], 
# "sensor_info": [{"bpm": , "temperature": , "altitude": , "location": }, {"bpm": , "temperature": , "altitude": , "location": }]}
# {"sensor_info": [{"name": , "time": , "bpm": , "temperature": , "altitude": , "location": }, {"name": , "time": , "bpm": , "temperature": , "altitude": , "location": }]}

for instance in sample_data:
    entry = {
        "batch": int(time.time()),
        "info": instance
    }

    # Create a document using the Database API.
    env_document = env_database.create_document(entry)

    # Check that the document exists in the database.
    if env_document.exists():
        print(f"Document '{instance[1]}' successfully created.")

result_collection = Result(env_database.all_docs)

print(f"Retrieved minimal document:\n{result_collection[0]}\n")

result_collection = Result(env_database.all_docs, include_docs=True)
print(f"Retrieved full document:\n{result_collection[0]}\n")

# try:
#     client.delete_database(database_name)
# except CloudantException:
#     print(f"There was a problem deleting '{database_name}'.\n")
# else:
#     print(f"'{database_name}' successfully deleted.\n")

client.disconnect()