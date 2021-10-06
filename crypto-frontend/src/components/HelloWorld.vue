<template>
  <v-container class="grey lighten-5">
    <v-row>
      <v-col >
        <v-btn
          fab
          color="blue"
          dark
          @click="sheet = !sheet"
          left
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-text-field
          v-model="num_of_USDT"
          label="NO. of USDT"
          hint="At least 1000"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="col-7">
        <v-card> 
          <v-card-title>
            <v-text-field
              v-model="search_str"
              append-icon="mdi-magnify"
              label="Search Coins"
              single-line
              hide-details
            ></v-text-field>
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
      <v-col class="col-5">
        <v-card
          class="mx-auto"
          v-if="selected_coin"
        >
          <v-row>
            <v-col class="col-3">
              <v-avatar
                size="120"
              >
                  <v-img
                    :src="`https://cdn.coindcx.com/static/coins/${selected_coin.currency.toLowerCase()}.svg`"
                  ></v-img>
              </v-avatar>
            </v-col>
            <v-col class="col-8">
              <v-list dense class="transparent">
                <v-list-item>
                  <!-- <v-list-item-icon>
                    <v-avatar
                      size="20px"
                    >
                    <v-img src="https://cdn.coindcx.com/static/coins/inr.svg" ></v-img>
                    </v-avatar>
                  </v-list-item-icon> -->

                  <v-list-item-title> Indian Rupee </v-list-item-title>
          
                  <v-list-item-subtitle class="text-right">
                    {{ user_available_inr }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <!-- <v-list-item-icon>
                    <v-avatar
                      size="20px"
                    >
                    <v-img src="https://cdn.coindcx.com/static/coins/usdt.svg" ></v-img>
                    </v-avatar>
                  </v-list-item-icon> -->

                  <v-list-item-title> US Dollar Token </v-list-item-title>
          
                  <v-list-item-subtitle class="text-right">
                    {{ user_available_usdt }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <!-- <v-list-item-icon>
                    <v-avatar
                      size="20px"
                    >
                    <v-img :src="`https://cdn.coindcx.com/static/coins/${selected_coin.currency.toLowerCase()}.svg`" ></v-img>
                    </v-avatar>
                  </v-list-item-icon> -->

                  <v-list-item-title> {{ selected_coin.coin_name }} </v-list-item-title>
          
                  <v-list-item-subtitle class="text-right">
                    {{ user_available_coin }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <!-- <v-list-item-icon>
                    <v-avatar
                      size="20px"
                    >
                    <v-img :src="`https://cdn.coindcx.com/static/coins/${selected_coin.currency.toLowerCase()}.svg`" ></v-img>
                    </v-avatar>
                  </v-list-item-icon> -->

                  <v-list-item-title> Predicted Profit </v-list-item-title>
          
                  <v-list-item-subtitle class="text-right">
                    {{ predicted_profit }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
          
          <v-card-title>{{ selected_coin.coin_name }}</v-card-title>
          
          <v-card-text>
             <v-stepper v-model="current_step">
              <v-stepper-header>
                <v-stepper-step
                  :complete="current_step > 1"
                  step="1"
                >
                  Buy USDT
                </v-stepper-step>

                <v-divider></v-divider>

                <v-stepper-step
                  :complete="current_step > 2"
                  step="2"
                >
                  {{ "Buy " + selected_coin.currency }} 
                </v-stepper-step>

                <v-divider></v-divider>

                <v-stepper-step step="3">
                  {{ "Sell " + selected_coin.currency }}
                </v-stepper-step>
              </v-stepper-header>

              <v-stepper-items>
                <v-stepper-content step="1">
                  <v-card
                    class="mb-12"
                    color="grey lighten-1"
                    height="200px"
                  >
                  
                  
                  
                  </v-card>

                  <v-btn text disabled>
                    Back
                  </v-btn>

                  <v-btn
                    color="primary"
                    @click="current_step = 2"
                  >
                    Next
                  </v-btn>

                </v-stepper-content>

                <v-stepper-content step="2">
                  <v-card
                    class="mb-12"
                    color="grey lighten-1"
                    height="200px"
                  ></v-card>

                  <v-btn text @click="current_step = 1">
                    Back
                  </v-btn>
                  
                  <v-btn
                    color="primary"
                    @click="current_step = 3"
                  >
                    Next
                  </v-btn>

                </v-stepper-content>

                <v-stepper-content step="3">
                  <v-card
                    class="mb-12"
                    color="grey lighten-1"
                    height="200px"
                  ></v-card>

                  <v-btn text @click="current_step = 2">
                    Back
                  </v-btn>

                  <v-btn
                    color="primary"
                    @click="current_step = 1"
                  >
                    Next
                  </v-btn>

                </v-stepper-content>
              </v-stepper-items>
            </v-stepper>
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
      current_step: 1,
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
      predicted_profit: 0
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
      console.log(item);
      this.selected_coin = item;
      this.predicted_profit = item['p&l'];
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
      axios.get(this.public_baseurl+"/market_data/orderbook",{
        pair: pair
      })
      .then((response) => {
        // console.log(response);
        console.log("GOt order book details for " + pair);
        this.coin_order_book[pair] = response.data;
      })
      .catch(function (error) {
        console.log(error);
        alert("Issue in getting market data");
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
        
        let transaction_fee = this.num_of_USDT * 0.08
        let inr_invested = (this.USDT_INR_price * this.num_of_USDT) + transaction_fee // INR -> USDT 
        
        transaction_fee = this.num_of_USDT/1000
        let num_of_AltCoin = (this.num_of_USDT - transaction_fee) / this.coin_of_interest[coin]['USDT']['last_price'] //USDT -> AltCoin

        transaction_fee = (num_of_AltCoin * this.coin_of_interest[coin]['INR']['last_price']) / 1000
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
    }
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

</style>
