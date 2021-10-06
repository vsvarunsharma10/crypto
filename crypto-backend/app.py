from flask import Flask, request, jsonify
# from flask import request
import requests
import json
import logging

import hmac
import hashlib
import base64
import json
import time
import requests

app = Flask(__name__)

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
KEY = "e6c1c79da1dccbd8cf60144293e3768e349c82415b460617"
SECRET = "97d13bbc79f1ef609fe7054744a66c1331323c55c959a9ad61df1e9d76187288"
SECRET_BYTES = bytes(SECRET, encoding='utf-8')


@app.route('/', methods=['GET', 'POST'])
# @app.route('/<path:path>', methods=['GET', 'POST']) # Enable when want to use 

# @cross_origin()
def index(path):
    headers = request.headers
    response = requests.post(path, data = json.loads(request.data), headers = headers)
    print(response) 
    data = response.json()
    # print(data) 
    # response.headers.add("Access-Control-Allow-Origin", "*") # Enabling Cors

    return jsonify(data)

@app.route('/user_details', methods=['GET', 'POST'])
def user_details():

    # Generating a timestamp
    timeStamp = int(round(time.time() * 1000))

    body = {
        "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(SECRET_BYTES, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/users/balances"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': KEY,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    return jsonify(data)


@app.route('/buy_sell_coins', methods=['POST'])
def buy_sell_coins():
    
    request_data = request.get_json()

    market = request_data['market']
    price_per_unit = request_data['market']
    total_quantity = request_data['total_quantity']

    # Generating a timestamp.
    timeStamp = int(round(time.time() * 1000))

    body = {
    "side": "buy",    #Toggle between 'buy' or 'sell'.
    "order_type": "limit_order", #Toggle between a 'market_order' or 'limit_order'.
    "market": market, #Replace 'SNTBTC' with your desired market pair.
    "price_per_unit": price_per_unit, #This parameter is only required for a 'limit_order'
    "total_quantity": total_quantity, #Replace this with the quantity you want
    "timestamp": timeStamp
    }

    json_body = json.dumps(body, separators = (',', ':'))

    signature = hmac.new(SECRET_BYTES, json_body.encode(), hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/orders/create"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data = json_body, headers = headers)
    data = response.json()
    print(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)