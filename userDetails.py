import hmac
import hashlib
import base64
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
key = "e6c1c79da1dccbd8cf60144293e3768e349c82415b460617"
secret = "97d13bbc79f1ef609fe7054744a66c1331323c55c959a9ad61df1e9d76187288"

# python3
# secret_bytes = bytes(secret, encoding='utf-8')
# python2
secret_bytes = bytes(secret)

# Generating a timestamp
timeStamp = int(round(time.time() * 1000))

body = {
    "timestamp": timeStamp
}

json_body = json.dumps(body, separators = (',', ':'))

signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

url = "https://api.coindcx.com/exchange/v1/users/balances"

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}

# response = requests.post(url, data = json_body, headers = headers)
# data = response.json();
# print(json.dumps(data));
print(json.dumps(json_body))

print(headers)
