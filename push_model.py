import urllib3, requests, json

# Paste your Watson Machine Learning service apikey here
# Use the rest of the code sample as written
apikey = "zFxCbxMvmnwCpLLRR6WfFravoB0Y8VjbEzCHyyH30oMo"

# Get an IAM token from IBM Cloud
url     = "https://iam.bluemix.net/oidc/token"
headers = { "Content-Type" : "application/x-www-form-urlencoded" }
data    = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
IBM_cloud_IAM_uid = "bx"
IBM_cloud_IAM_pwd = "bx"
response  = requests.post( url, headers=headers, data=data, auth=( IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd ) )
iam_token = response.json()["access_token"]

# NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token, 'ML-Instance-ID': "c72ce2ad-4d0e-4a9c-ab02-d5a113a8c990"}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"fields": ["f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19"],
"values": [[1.0, 2.3, 15.0, 12.1, 3.0, 1.0, 2.3, 15.0, 12.1, 3.0, 1.0, 2.3, 15.0, 12.1, 3.0, 1.0, 2.3, 15.0, 12.1, 2.1]]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/v3/wml_instances/c72ce2ad-4d0e-4a9c-ab02-d5a113a8c990/deployments/9e0670ea-2bca-48c5-85d6-9d197555a326/online', json=payload_scoring, headers=header)
print("Scoring response")
print(json.loads(response_scoring.text))
