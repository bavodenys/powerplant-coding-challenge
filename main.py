import requests
import os
import json

API_URL = "http://127.0.0.1:8888/"
PAYLOAD_FOLDER = "example_payloads"
RESPONSE_FOLDER = "example_response"

if __name__ == "__main__":
    # Test the API connection
    req = requests.get(API_URL)
    if req.status_code == 200:
        # Get payload examples from the payload folder
        payloads = os.listdir(PAYLOAD_FOLDER)
        for payload in payloads:
            with open(f'{PAYLOAD_FOLDER}/{payload}', 'r') as f:
                data = json.load(f)
                result = requests.post(API_URL + "/productionplan", json=data).json()
                f.close()
            with open(f"{RESPONSE_FOLDER}/response_{payload}", "w") as f:
                json.dump(result, f)
                f.close()
    else:
        print('Test of API connection was not successful')


