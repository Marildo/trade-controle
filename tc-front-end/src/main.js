import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

import './plugins/graphql'

import Vue from 'vue'
import App from './App.vue'
import store from './config/store'
import router from './router'


Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
