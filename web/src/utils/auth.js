import Cookies from 'js-cookie'

const TokenKey = 'access_token'
const TokenKeyTime = `${TokenKey}_time`
const RefreshKey = 'refresh_token'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function getTokenTime() {
  return Cookies.get(TokenKeyTime)
}

export function setToken(token) {
  if (!token) token = '' // 当token为undefined时，存入cookies后变成了字符串'undefined'
  else Cookies.set(TokenKeyTime, Date.now())
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  Cookies.remove(TokenKeyTime)
  return Cookies.remove(TokenKey)
}

export function getRefresh() {
  return Cookies.get(RefreshKey)
}

export function setRefresh(token) {
  if (!token) token = '' // 当token为undefined时，存入cookies后变成了字符串'undefined'
  return Cookies.set(RefreshKey, token)
}

export function removeRefresh() {
  return Cookies.remove(RefreshKey)
}
