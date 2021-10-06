// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import vuetify from './plugins/vuetify'

Vue.config.silent = true

Vue.config.productionTip = false


import Cryptoicon from 'vue-cryptoicon';
import icon from 'vue-cryptoicon/src/icons';
Cryptoicon.add(icon);
Vue.use(Cryptoicon);


Vue.mixin({
  data: function () {
    return {
      baseurl : "https://api.coindcx.com",
      public_baseurl : "https://public.coindcx.com",
      cors_server_url: window.location.origin.replace(":8080", ":8000/"), // MIGHT BREAK AFTER CHANGING PORT OF VUEJS DEVELOPEMENT SERVER PORT
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  vuetify,
  template: '<App/>'
})
