import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/sxcapi-dtm/token/obtain/',
    method: 'post',
    data
  })
}

export function refresh(data) {
  return request({
    url: '/sxcapi-dtm/token/refresh/',
    method: 'post',
    data
  })
}

export function getInfo() {
  return request({
    url: '/sxcapi-dtm/user/info/',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/sxcapi-dtm/user/logout/',
    method: 'post'
  })
}
