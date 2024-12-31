import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import '@/icons' // icon
import '@/permission' // permission control

// set ElementUI lang to EN
// Vue.use(ElementUI, { locale })
// 如果想要中文版 element-ui，按如下方式声明
Vue.use(ElementUI)

// Vue.config.productionTip = false

// RSA 加密，全局挂载
import defaultSettings from '@/settings'
import { JSEncrypt } from 'jsencrypt'
Vue.prototype.$rsaEncrypt = function(password) {
  const js_encrypt = new JSEncrypt()
  // 公钥是与后端私钥匹配的，一般是后端生成并提供【本项目图省事采取固定密钥对，若想更安全，可采取动态密钥，每次从后端获取】
  js_encrypt.setPublicKey(defaultSettings.pubkey)
  return js_encrypt.encrypt(password)
}

// 监听鼠标、键盘事件，刷新token
import { addListener } from '@/views/common/js/listener'
import { refreshToken } from '@/views/common/js/requestHandle'
addListener(['mousedown', 'keydown', 'scroll'], refreshToken)

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
