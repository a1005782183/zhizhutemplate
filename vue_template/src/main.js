// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import $ from 'jquery'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
// 导入路由的包
import VueRouter from 'vue-router'
// 安装路由
Vue.use(VueRouter)
// 挂在Axios到全局
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
Vue.prototype.$axios = axios;
Vue.prototype.HOST = '/zzt'
axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://127.0.0.1:5000/';

import router from './router.js'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

