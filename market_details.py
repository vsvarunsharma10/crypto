import requests # Install requests module first.

def get_market_details():
    url = "https://api.coindcx.com/exchange/v1/markets_details"
    response = requests.get(url)
    data = response.json()
    return data

final_data = {}


data = get_market_details()

for x in data:
    if "INR" in x["pair"] and x["target_currency_name"] not in final_data:
        final_data[x["target_currency_name"]]  = {"INR": {"pair":x["pair"], "order_types":x["order_types"]}}

for x in data:
    if x["target_currency_name"] in final_data:
        if "USDT" in x["pair"]:
            final_data[x["target_currency_name"]]["USDT"] = { "pair" : x["pair"], "order_types": x["order_types"]}
           

for x in final_data.keys():
    if "USDT" not in final_data[x] or "INR" not in final_data[x]:
        del final_data[x]

print(final_data)