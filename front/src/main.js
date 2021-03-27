import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'

import store from './store'

import './plugins/bootstrap-vue'
import './plugins/axios-vue'
import './plugins/markdown'

import App from './App.vue'
import router from './router'
import { i18n } from './i18n'

new Vue({
  router,
  i18n,
  render: h => h(App),
  store
}).$mount('#app')
