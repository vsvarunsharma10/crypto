<template>
  <v-container class="mt-2" style="max-width: 100%!important;">
    <v-row>
      <v-col class="col-7">
        <v-card> 
          <v-card-title>
            <v-row>
              <v-col class="col-1" >
                <v-btn x-small fab @click="sheet = !sheet" left >
                  <v-avatar size="32px" >
                    <v-img src="https://cdn.coindcx.com/static/coins/inr.svg"></v-img>
                  </v-avatar>
                </v-btn>
             </v-col>
              <v-col class="font-size:10px">
                <span >
                {{ "INR : "+user_available_inr }}
                </span>
              </v-col>
              <v-col>
                {{ "USDT : "+user_available_usdt }}
              </v-col>
              <v-col class="col-2">
                <v-text-field style="margin:0px; padding:0px;"
                  v-model="num_of_USDT"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="mt-0">
              <v-text-field class="mt-0 pt-0"
                v-model="search_str"
                append-icon="mdi-magnify"
                label="Search Coins"
                single-line
                hide-details
              ></v-text-field>
            </v-row>
          </v-card-title>
          <v-data-table
            :search="search_str"
            filterable
            @click:row="select_currency"
            :headers="headers"
            :items="coin_price_data"
            item-key="name"
            loading_data
            loading-text="Loading... Please wait"
            class="elevation-1"
            :sort-by="['p&l']"
            :sort-desc="[true]"
            :items-per-page="7"
          >
            <template v-slot:item.coin_name="{ item }">
              <span>
                <v-avatar
                  size="20px"
                >
                  <v-img
                    :src="`https://cdn.coindcx.com/static/coins/${item.currency.toLowerCase()}.svg`"
                  ></v-img>
                </v-avatar>
                {{ item.coin_name }} 
                <!-- {{ item.currency }} -->
              </span>
              
            </template>
          </v-data-table>
        </v-card>
      </v-col>
      <v-col class="col">
        <v-card  class="mx-auto" v-if="selected_coin">
          <v-row>
            <v-col class="col-2">
              <div class="ml-5">
                <v-avatar size="70" >
                    <v-img :src="`https://cdn.coindcx.com/static/coins/${selected_coin.currency.toLowerCase()}.svg`" ></v-img>
                </v-avatar>
              </div>
            </v-col>
            <v-col >
              <v-card-title>{{ selected_coin.coin_name + " : " + user_available_coin}}</v-card-title>
            </v-col>
            <v-col>
              <v-list dense class="transparent">
                <v-list-item>
                  <v-list-item-title> Predicted Profit </v-list-item-title>
                  <v-list-item-subtitle class="text-right">
                    {{ predicted_profit }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title> Current Profit </v-list-item-title>
                  <v-list-item-subtitle class="text-right">
                    {{ predicted_profit }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
          
          <v-card-text>
            <v-card>
              <v-tabs v-model="current_step">
                <v-tab>
                  Buy USDT
                </v-tab>
                <v-tab> 
                  Buy AltCoin
                </v-tab>
                <v-tab>
                  Sell AltCoin
                </v-tab>
              </v-tabs>

              <v-tabs-items v-model="current_step">
                <v-tab-item>
                  <v-card flat>
                    <v-card-text v-if='order_book_data["I-USDT_INR"]'>
                      <v-row>
                        <v-col style="overflow: auto;height: 40vh">
                          Asks
                          <v-data-table
                            dense
                            :headers='[{"text": "Price", "value":"price"}, {"text":"Qty", "value":"qty"}]'
                            :items='order_book_data["I-USDT_INR"]["asks"]'
                            item-key="name"
                            :sort-by="['price']"
                            :sort-desc="[false]"
                            class="elevation-1"
                            hide-default-footer
                          ></v-data-table>
                        </v-col>
                        <v-col style="overflow: auto; height: 40vh">    
                          Bids
                          <v-data-table
                            dense
                            :headers='[{"text": "Price", "value":"price"}, {"text":"Qty", "value":"qty"}]'
                            :items='order_book_data["I-USDT_INR"]["bids"]'
                            item-key="name"
                            :sort-by="['price']"
                            :sort-desc="[true]"
                            class="elevation-1"
                            hide-default-footer
                          ></v-data-table>
                        </v-col>
                      </v-row>    
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item>
                  <v-card flat>
                    <v-card-text v-if='order_book_data[coin_of_interest[selected_coin.coin_name]["USDT"]["pair"]]'>
                      <v-row>
                        <v-col style="overflow: auto; height: 40vh">
                          Asks 
                          <v-data-table
                            dense
                            :headers='[{"text": "Price", "value":"price"}, {"text":"Qty", "value":"qty"}]'
                            :items='order_book_data[coin_of_interest[selected_coin.coin_name]["USDT"]["pair"]]["asks"]'
                            item-key="name"
                            :sort-by="['price']"
                            :sort-desc="[false]"
                            class="elevation-1"
                            hide-default-footer
                          ></v-data-table>
                        </v-col>
                        <v-col style="overflow: auto; height: 40vh">  
                          Bids    
                          <v-data-table
                            dense
                            :headers='[{"text": "Price", "value":"price"}, {"text":"Qty", "value":"qty"}]'
                            :items='order_book_data[coin_of_interest[selected_coin.coin_name]["USDT"]["pair"]]["bids"]'
                            item-key="name"
                            :sort-by="['price']"
                            :sort-desc="[true]"
                            class="elevation-1"
                            hide-default-footer
                          ></v-data-table>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-tab-item>
                <v-tab-item>
                  <v-card flat>
                    <v-card-text v-if='order_book_data[coin_of_interest[selected_coin.coin_name]["INR"]["pair"]]'>
                      <v-row>
                        <v-col style="overflow: auto;height: 40vh">  
                          Asks 
                          <v-data-table
                            dense
                            :headers='[{"text": "Price", "value":"price"}, {"text":"Qty", "value":"qty"}]'
                            :items='order_book_data[coin_of_interest[selected_coin.coin_name]["INR"]["pair"]]["asks"]'
                            item-key="name"
                            :sort-by="['price']"
                            :sort-desc="[false]"
                            class="elevation-1"
                            hide-default-footer
                          ></v-data-table>
                        </v-col>
                        <v-col style="overflow: auto;height: 40vh">
                          Bids       
                          <v-data-table
                            dense
                            :headers='[{"text": "Price", "value":"price"}, {"text":"Qty", "value":"qty"}]'
                            :items='order_book_data[coin_of_interest[selected_coin.coin_name]["INR"]["pair"]]["bids"]'
                            item-key="name"
                            :sort-by="['price']"
                            :sort-desc="[true]"
                            class="elevation-1"
                            hide-default-footer
                          ></v-data-table>
                          </v-col>
                      </v-row> 
                    </v-card-text>
                  </v-card>
                </v-tab-item>
              </v-tabs-items>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-bottom-sheet v-model="sheet">
      <v-sheet
        class="text-center"
      >
        <v-data-table
          :headers="user_balance_headers"
          :items="user_owned_coins"
          item-key="name"
          loading_data
          loading-text="Loading... Please wait"
          class="elevation-1"
          :sort-by="['balance']"
          :sort-desc="[true]"
        >
          <template v-slot:item.currency="{ item }">
            <span>
              <v-avatar
                  size="20px"
                >
                  <v-img
                    :src="`https://cdn.coindcx.com/static/coins/${item.currency.toLowerCase()}.svg`"
                  ></v-img>
                </v-avatar>
              {{ item.currency }}
            </span>
          </template>
        </v-data-table>
      </v-sheet>
    </v-bottom-sheet>
  </v-container>
</template>

<script>
import io from 'socket.io-client';
const axios = require('axios');
const crypto = require('crypto');

export default {
  name: 'HelloWorld',
  data () {
    return {
      current_step: 0,
      search_str: '',
      drawer: true,
      sheet: false,
      loading_data: true,
      selected_coin: undefined,
      coin_market_name_mapping : {},
      market_details : {},
      coin_of_interest : {},
      coin_order_book : {},
      coin_trade_history : {},
      ticker_data : {},
      ticker_frequency : 1000, // 1 sec
      num_of_USDT : 1000,
      USDT_INR_price : 0,
      USDT_INR_market_name : "USDTINR",
      headers: [
          {text: 'Coin name',value: 'coin_name', align: 'start' },
          { text: 'USDT Price', value: 'usdt_price' },
          // { text: 'USDT Order Types', value: 'usdt_order_type' },
          { text: 'INR Price', value: 'inr_price' },
          // { text: 'INR Order Types', value: 'inr_order_types' },
          { text: 'Returned - Invested', value: 'invested_&_returned' },
          { text: 'P&L', value: 'p&l' }
        ],
      user_balance_headers: [
          {text: 'Coin name',value: 'currency', align: 'start' },
          { text: 'Avaialble Balance', value: 'balance' },
          { text: 'Locked Balance', value: 'locked_balance' }
        ],
      coin_price_data:[],
      user_owned_coins:[],
      user_available_coin: 0,
      predicted_profit: 0,
      market_order_book_intervals:[],
      order_book_data:{},
      fastest_usdt_price:0,
      fastest_usdt_to_coin_price:0,
      fastest_coint_to_inr:0
    }
  },
  mounted(){
    this.__get_market_details();
    this.__get_user_details();
    setInterval(()=>{ this.__get_market_ticker() }, this.ticker_frequency);
  },
  methods:{
    buy_usdt(price_per_unit , quantity){

      axios.post(this.cors_server_url+'http://172.29.1.2:5000/buy_sell_coins', {
        market : 'USDTINR',
        price_per_unit : price_per_unit,
        quantity : quantity
      })
      .then((response) => {
        // console.log(response);
        this.market_details = response.data;
      })
      .catch(function (error) {
        console.log(error);
        alert("Issue in getting market data");
      }) 

    },
    select_currency(item){
      this.market_order_book_intervals.forEach(element => {
        clearInterval(element);
      });
      this.market_order_book_intervals=[];
      console.log(item);
      this.selected_coin = item;
      this.predicted_profit = item['p&l'];
      this.order_book_data = {};
      this.market_order_book_intervals.push(setInterval(()=>{ this.__get_order_book(this.coin_of_interest[item['coin_name']]['USDT']['pair']); }, 2000));
      this.market_order_book_intervals.push(setInterval(()=>{ this.__get_order_book(this.coin_of_interest[item['coin_name']]['INR']['pair']); }, 2000));
      this.market_order_book_intervals.push(setInterval(()=>{ this.__get_order_book("I-USDT_INR"); }, 2000));
    },
    __get_market_details(){
      this.loading_data = true;
      axios.get(this.cors_server_url+this.baseurl+'/exchange/v1/markets_details')
      .then((response) => {
        // console.log(response);
        // console.log("GOt market Data");
        this.market_details = response.data;
      })
      .catch(function (error) {
        console.log(error);
        alert("Issue in getting market data");
      }) 
    },
    __filter_coins(){
      
      let coin_of_interest = {}

      for(let coin of this.market_details){
        this.coin_market_name_mapping[coin["symbol"]] = coin["target_currency_name"];
        if( coin["pair"].includes("INR") && !(coin["target_currency_name"] in coin_of_interest))
          coin_of_interest[coin["target_currency_name"]] = {"INR": {"pair":coin["pair"], "order_types":coin["order_types"]}, "currency":coin["target_currency_short_name"]}
      }

      for(let coin of this.market_details){
        if( coin["pair"].includes("USDT") && coin["target_currency_name"] in coin_of_interest){
          coin_of_interest[coin["target_currency_name"]]["USDT"] = {"pair":coin["pair"], "order_types":coin["order_types"]}
        }
      }

      for(let coin in coin_of_interest){
        // coin = coin_of_interest[coin];
        if( !("USDT" in coin_of_interest[coin] ) || !("INR" in coin_of_interest[coin] ))
          delete coin_of_interest[coin];
      }

      this.coin_of_interest = coin_of_interest;
      this.loading_data = false;
    },
    __get_order_book(pair){
      axios.get(this.public_baseurl+"/market_data/orderbook?pair="+pair)
      .then((response) => {
        // console.log("GOt order book details for " + pair);
        this.order_book_data[pair] = {"bids":[], "asks":[]};
        Object.entries(response.data.bids).forEach(([price, qty]) => { this.order_book_data[pair]["bids"].push({"qty":qty, "price": price}); });
        Object.entries(response.data.asks).forEach(([price, qty]) => { this.order_book_data[pair]["asks"].push({"qty":qty, "price": price}); });
      })
      .catch(function (error) {
        console.log(error);
        alert("Issue in getting order book data of "+pair);
      }) 
    },
    __get_trade_history(pair, limi=30){
      axios.get(this.public_baseurl+"/market_data/trade_history",{
        pair: pair,
        limit:limit
      })
      .then((response) => {
        // console.log(response);
        console.log("GOt trade details for " + pair);
        this.coin_trade_history[pair] = response.data;
      })
      .catch(function (error) {
        console.log(error);
        alert("Issue in getting trade history data");
      }) 
    },
    __get_market_ticker(){
      axios.get(this.baseurl+"/exchange/ticker")
      .then((response) => {
        // console.log(response);
        // console.log("GOt tiker details");
        // this.ticker_data = response.data;
        this.__process_ticker_data(response.data);
      })
      .catch(function (error) {
        console.log(error);
        alert("Issue in getting ticker data");
      }) 
    },
    __process_ticker_data(ticker_data){    
      
      let temp_data = Object.assign({}, this.coin_of_interest);
      
      for(let index in ticker_data){
        let market = ticker_data[index];
        if(market==undefined) break;
        if(market['market']==this.USDT_INR_market_name) this.USDT_INR_price = market['last_price']; 
        if(this.coin_market_name_mapping[market['market']] in temp_data){
          if(market['market'].includes("INR"))temp_data[this.coin_market_name_mapping[market['market']]]['INR']['last_price'] = market['last_price'];
          if(market['market'].includes("USDT")) temp_data[this.coin_market_name_mapping[market['market']]]['USDT']['last_price'] = market['last_price']; 
        }
      }

      this.coin_of_interest = temp_data;

    },
    __get_user_details(){
      axios.post(this.cors_server_url+'http://172.29.1.2:5000/user_details')
      .then((response) => {
        // console.log(response);
        this.user_owned_coins = response.data;
        // console.log("GOt user details");
        // this.ticker_data = response.data;
      })
      .catch(function (error) {
        console.log(error);
        alert("Issue in getting User data");
      }) 
    },
    evaluate_coin_prices(pair){
      // console.log("Evaluating the market prices");
      let new_prices = [];

      for(let coin in this.coin_of_interest){
        
        let transaction_fee = (this.USDT_INR_price * this.num_of_USDT) / 1000 // fee is 0.1%
        let inr_invested = (this.USDT_INR_price * this.num_of_USDT) + transaction_fee // INR -> USDT 
        
        transaction_fee = this.num_of_USDT / 500 // fee is 0.2%          
        let num_of_AltCoin = (this.num_of_USDT - transaction_fee) / this.coin_of_interest[coin]['USDT']['last_price'] //USDT -> AltCoin

        transaction_fee = (num_of_AltCoin * this.coin_of_interest[coin]['INR']['last_price']) / 500 // fee is 0.2 %
        let inr_returned = (num_of_AltCoin * this.coin_of_interest[coin]['INR']['last_price']) - transaction_fee // AltCoin -> INR 

        let p_and_l = inr_returned - inr_invested;

        new_prices.push({
          "coin_name" : coin, 
          "inr_price" : this.coin_of_interest[coin]['INR']['last_price'],
          "inr_order_types" : this.coin_of_interest[coin]['INR']['order_types'],
          "usdt_price" : this.coin_of_interest[coin]['USDT']['last_price'],
          "usdt_order_type" : this.coin_of_interest[coin]['USDT']['order_types'],
          "invested_&_returned" : inr_returned.toFixed(3).toString()+" - "+inr_invested.toFixed(3).toString(),
          "p&l" : p_and_l.toFixed(3),
          "currency" : this.coin_of_interest[coin].currency
        });
      }

      this.coin_price_data = new_prices;
    },
    evaluate_user_available_coin(){
        if(!this.selected_coin) return 0;
        console.log("Currency changed value changed");
        let currency = this.selected_coin.currency;
        if(this.user_owned_coins.length == 0) return 0;
        let coin = this.user_owned_coins.filter((coin)=> {  return coin.currency == currency });
        this.user_available_coin =  coin[0]["balance"]
    },
  },
  computed:{
    user_available_inr(){
        if(this.user_owned_coins.length == 0) return 0;
        let inr_coin = this.user_owned_coins.filter((coin)=> {  return coin.currency == "INR" });
        return inr_coin[0]["balance"]
    },
    user_available_usdt(){
        if(this.user_owned_coins.length == 0) return 0;
        let inr_coin = this.user_owned_coins.filter((coin)=> {  return coin.currency == "USDT" });
        return inr_coin[0]["balance"]
    },
    selected_coin_current_order_book_cal(){
      this.fastest_usdt_price

      return 0
    }
  },
  watch:{
    market_details(){

      this.__filter_coins();
    },
    ticker_data(){
      console.log("Ticker changed");
    },
    coin_of_interest(){
      // console.log("Evaluated the values");
      this.evaluate_coin_prices();
      this.evaluate_user_available_coin();
    },
    num_of_USDT(){
      this.evaluate_coin_prices();
    }
  }
}
</script>

<style>
/* width */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
 
/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}
</style>
