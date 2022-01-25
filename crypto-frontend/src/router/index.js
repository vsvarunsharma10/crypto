import Vue from 'vue'
import Router from 'vue-router'
import CoinDCX from '@/components/CoinDCX'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: CoinDCX
    },
    {
      path: '/coindcx',
      name: 'CoinDCX',
      component: CoinDCX
    }
  ]
})
