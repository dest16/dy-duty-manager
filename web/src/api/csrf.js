import request from '@/utils/request'
import { setCSRFToken } from '@/utils/csrf'

export function getCSRFToken() {
  return request({
    url: '/sxcapi-dtm/csrf-token/',
    method: 'get',
    // 访问后端时，若出现csrf错误，请启用transformResponse
    transformResponse: [
      function(data) {
        // 如果返回数据中csrfToken存在，则保存到cookies
        try {
          setCSRFToken(JSON.parse(data)['csrfToken'])
        } catch (e) {
          console.log('请求csrfToken时出错！')
        }
      }
    ]
  })
}
