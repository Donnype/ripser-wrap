import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import './filters'

global.jQuery = require('jquery')
let $ = global.jQuery
window.$ = $

$(function () {
  $('[data-toggle="popover"]').popover()
})

$('.popover-dismiss').popover({
  trigger: 'focus'
})

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
