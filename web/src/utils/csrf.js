import Cookies from 'js-cookie'

const CSRFTokenKey = 'X-CSRFToken'

export function getCSRFToken() {
  return Cookies.get(CSRFTokenKey)
}

export function setCSRFToken(token) {
  return Cookies.set(CSRFTokenKey, token)
}

export function removeCSRFToken() {
  return Cookies.remove(CSRFTokenKey)
}
