import json
import requests
from tqdm import tqdm
from prettytable import PrettyTable

# Logic

# Cost for USDT = (USDT price INR  * NO. Of Tokens ) + Trans. charges (NO. Of Tokens * 0.08)

# NO. of XRP = No. USDT tokens / Price of 1 XRP with respect to USDT

# XRP value = (XRP price INR * no. of XRP) - Transc. charges

# Profit / Loss = XRP value - Cost of USDT

# API KEY - e6c1c79da1dccbd8cf60144293e3768e349c82415b460617
# API SECRET - 97d13bbc79f1ef609fe7054744a66c1331323c55c959a9ad61df1e9d76187288

def __get_raw_market_details():
    url = "https://api.coindcx.com/exchange/v1/markets_details"
    response = requests.get(url)
    data = response.json()
    return data

def __get_order_book(pair):
    url = "https://public.coindcx.com/market_data/orderbook?pair="+pair 
    response = requests.get(url)
    data = response.json()
    # {"price":"Qty"}
    return data

def __get_trade_history(pair, limit=30):
    url = "https://public.coindcx.com/market_data/trade_history?pair="+pair+"&limit="+str(limit) 
    response = requests.get(url)
    data = response.json()
    return data

def cal_current_price(pair):

    price = {}
    trade_history = __get_trade_history(pair, 30)
    order_book = __get_order_book(pair)
    # print(json.dumps(order_book))
    # exit()
    current_price = 0

    # price['ask_nearest_to_last_price'] = order_book['asks'][]
    # price['bid_nearest_to_last_price'] = order_book['bids'][]

    for trade in trade_history:
        current_price += trade['p']

    # for ask in order_book['asks']:
    #     if  ask

    

    avg_price = current_price/len(trade_history)
    price['avg_price'] = avg_price

    last_price = trade_history[-1]['p']
    price['last_price'] = last_price

    delta = avg_price - last_price
    price['delta'] = delta

    if delta < 0:
        price["direction"] = "DOWN"
    else:
        price['direction'] = "UP"

    return price

def get_market_details():
    market_details = {}

    raw_data = __get_raw_market_details()
    
    # Collecting all INR
    for coin in raw_data:
        if "INR" in coin["pair"] and coin["target_currency_name"] not in market_details:
            market_details[coin["target_currency_name"]]  = {"INR": {"pair":coin["pair"], "order_types":coin["order_types"]}}
    
    # Collect USDT and that are already collected for INR
    for coin in raw_data:
        if coin["target_currency_name"] in market_details:
            if "USDT" in coin["pair"]:
                market_details[coin["target_currency_name"]]["USDT"] = { "pair" : coin["pair"], "order_types": coin["order_types"]}
            
    #  Cleaning the coins that are onlyavilable for INR and not for USDT
    for coin in market_details.keys():
        if "USDT" not in market_details[coin] or "INR" not in market_details[coin]:
            del market_details[coin]

    return market_details

# market_details = {'Chromia': {'USDT': {'pair': 'B-CHR_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-CHR_INR', 'order_types': ['limit_order']}}, 'Chiliz': {'USDT': {'pair': 'B-CHZ_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-CHZ_INR', 'order_types': ['limit_order']}}, 'Litecoin': {'USDT': {'pair': 'B-LTC_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-LTC_INR', 'order_types': ['limit_order']}}, 'yearn.finance': {'USDT': {'pair': 'B-YFI_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-YFI_INR', 'order_types': ['limit_order']}}, 'Theta Token': {'USDT': {'pair': 'B-THETA_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-THETA_INR', 'order_types': ['limit_order']}}, 'Binance Coin': {'USDT': {'pair': 'B-BNB_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-BNB_INR', 'order_types': ['limit_order']}}, 'Polkadot': {'USDT': {'pair': 'B-DOT_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-DOT_INR', 'order_types': ['limit_order']}}, 'Doge': {'USDT': {'pair': 'B-DOGE_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-DOGE_INR', 'order_types': ['limit_order']}}, 'Bitcoin': {'USDT': {'pair': 'B-BTC_USDT', 'order_types': ['take_profit_market', 'take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-BTC_INR', 'order_types': ['market_order', 'limit_order']}}, 'EOS': {'USDT': {'pair': 'B-EOS_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-EOS_INR', 'order_types': ['limit_order']}}, 'Stellar Lumens': {'USDT': {'pair': 'B-XLM_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-XLM_INR', 'order_types': ['limit_order']}}, 'Basic Attention Token': {'USDT': {'pair': 'B-BAT_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-BAT_INR', 'order_types': ['limit_order']}}, 'Ethereum': {'USDT': {'pair': 'B-ETH_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-ETH_INR', 'order_types': ['limit_order']}}, 'Uniswap': {'USDT': {'pair': 'B-UNI_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-UNI_INR', 'order_types': ['limit_order']}}, 'Harmony': {'USDT': {'pair': 'B-ONE_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-ONE_INR', 'order_types': ['limit_order']}}, 'STP Network': {'USDT': {'pair': 'B-STPT_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-STPT_INR', 'order_types': ['limit_order']}}, 'USD Coin': {'USDT': {'pair': 'B-USDC_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-USDC_INR', 'order_types': ['limit_order']}}, 'Enjin Coin': {'USDT': {'pair': 'B-ENJ_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-ENJ_INR', 'order_types': ['limit_order']}}, 'Crypto.com Coin': {'USDT': {'pair': 'H-CRO_USDT', 'order_types': ['limit_order']}, 'INR': {'pair': 'I-CRO_INR', 'order_types': ['limit_order']}}, 'Cardano': {'USDT': {'pair': 'B-ADA_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-ADA_INR', 'order_types': ['limit_order']}}, 'Bitcoin Cash': {'USDT': {'pair': 'B-BCH_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-BCH_INR', 'order_types': ['limit_order']}}, 'Tron': {'USDT': {'pair': 'B-TRX_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-TRX_INR', 'order_types': ['limit_order']}}, 'VeChain': {'USDT': {'pair': 'B-VET_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-VET_INR', 'order_types': ['limit_order']}}, 'Matic Network': {'USDT': {'pair': 'B-MATIC_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-MATIC_INR', 'order_types': ['limit_order']}}, 'Chainlink': {'USDT': {'pair': 'B-LINK_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-LINK_INR', 'order_types': ['limit_order']}}, 'Ripple': {'USDT': {'pair': 'B-XRP_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-XRP_INR', 'order_types': ['limit_order']}}, 'Tether': {'USDT': {'pair': 'I-USDT_INR', 'order_types': ['limit_order']}, 'INR': {'pair': 'I-USDT_INR', 'order_types': ['limit_order']}}, 'Orchid': {'USDT': {'pair': 'B-OXT_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-OXT_INR', 'order_types': ['limit_order']}}, 'Swipe': {'USDT': {'pair': 'B-SXP_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-SXP_INR', 'order_types': ['limit_order']}}, 'Nervos': {'USDT': {'pair': 'B-CKB_USDT', 'order_types': ['take_profit', 'stop_limit', 'market_order', 'limit_order']}, 'INR': {'pair': 'I-CKB_INR', 'order_types': ['limit_order']}}}

ORDER_TYPE_MAPPING = {
    "limit_order" : "LMT",
    "market_order" : "MRKT",
    # Addd more if required
}


if __name__=="__main__":

    # print(json.dumps(__get_order_book("I-XRP_INR")))
    # exit()

    table = PrettyTable(['Coin Name', 'INR Price', 'INR Order Types', 'USDT Price', 'USDT Order Types', "Invested - Returned" ,'P&L'])
    table.align["Coin Name"] = "l"
    table.align["Delta Profit/Loss"] = "r"

    market_details = get_market_details()

    coin_details_itr = tqdm(market_details, desc="Transform ")

    for coin in coin_details_itr:

        coin_details_itr.set_description("Transform : " + coin)

        INR_market = market_details[coin]["INR"]["pair"]
        USDT_market = market_details[coin]["USDT"]["pair"]

        AltCoin_price_INR_data = cal_current_price(INR_market)  
        AltCoin_price_USDT_data = cal_current_price(USDT_market)
        USDT_price_INR_data = cal_current_price("I-USDT_INR")

        num_of_coin = 1000

        # print("INR -> USDT -> AltCoin -> INR")
        transaction_fee = num_of_coin * 0.08
        USDT_cost_in_INR = (USDT_price_INR_data["last_price"] * num_of_coin ) + transaction_fee # INR -> USDT
        # print("Invested " + str(USDT_cost_in_INR))

        transaction_fee = num_of_coin/1000
        num_of_AltCoin = (num_of_coin - transaction_fee) / AltCoin_price_USDT_data["avg_price"] # USDT -> AltCoin
        # print(num_of_AltCoin)

        transaction_fee = (num_of_AltCoin * AltCoin_price_INR_data["avg_price"]) / 1000
        dilluting_AltCoin = (num_of_AltCoin * AltCoin_price_INR_data["avg_price"]) - transaction_fee # AltCoin -> INR 
        # print("Returned " + str(dilluting_AltCoin))

        returned_value = dilluting_AltCoin - USDT_cost_in_INR
        # print("Delta " +  str(returned_value))

        INR_order_types = ", ".join(filter(lambda y: (y != None) ,map(lambda x: ORDER_TYPE_MAPPING.get(x), market_details[coin]["INR"]['order_types'])))
        USDT_order_types = ", ".join(filter(lambda y: (y != None) ,map(lambda x: ORDER_TYPE_MAPPING.get(x), market_details[coin]["USDT"]['order_types'])))

        table.add_row([ coin, AltCoin_price_INR_data['avg_price'], INR_order_types, AltCoin_price_USDT_data['avg_price'], USDT_order_types, "{} - {} =".format(USDT_cost_in_INR, dilluting_AltCoin), returned_value])

    table.sortby = "P&L"


    print
    print("USDT INR Market" + str(USDT_price_INR_data) )
    print
    print(table)

