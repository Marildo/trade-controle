import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';

import './plugins/graphql'
import './plugins/primevue'

Vue.config.productionTip = false

import { formaterReal } from "@/lib/numberUtils";

Vue.filter('formaterReal', (value) => formaterReal(value))


new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')