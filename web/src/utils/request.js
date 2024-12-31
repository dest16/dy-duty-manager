import axios from 'axios'
import { Message } from 'element-ui'
import { getToken, removeRefresh, removeToken } from '@/utils/auth'
import { getCSRFToken, removeCSRFToken } from '@/utils/csrf'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = common url + request url
  withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    const access_token = getToken()
    if (access_token) {
      // 后端jwt设置了'AUTH_HEADER_TYPES': ('Bearer',)，因此Authorization必须格式如：Bearer <token>
      config.headers.Authorization = `Bearer ${access_token}`
    }

    // 访问后端时，若出现csrf错误，请启用下列两行代码
    const csrfToken = getCSRFToken()
    if (csrfToken) config.headers['X-CSRFToken'] = csrfToken

    config.headers['Content-Type'] = 'application/json'
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => {
    const data = response.data
    const status = response.status
    return {
      data,
      status
    }
  },
  async error => { // 大于4xx的返回都为被认为是error
    const response = error.response
    const status = response.status

    // 获取当前页面url，判断是否是 login 页面，如果是则不做401的处理
    const url = window.location.href
    const path = url.split('/').slice(3).join('/')
    const isLogin = path.substr(0, 7) === '#/login' || path.substr(0, 6) === '/login'

    if (status === 401 && !isLogin) {
      removeToken() // must remove  token  first
      removeRefresh()
      removeCSRFToken()
      window.location.href = '/' // 跳转到首页，若首页需登录会自动触发权限管理代码，重定向到login页面
    } else if (status < 500) {
      const data = response.data
      return {
        data,
        status
      }
    }
    console.log('err' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
