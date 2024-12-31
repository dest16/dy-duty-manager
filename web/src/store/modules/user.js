import { Message } from 'element-ui'
import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken, getRefresh, setRefresh, removeRefresh } from '@/utils/auth'
import { removeCSRFToken } from '@/utils/csrf'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    refresh: getRefresh(),
    name: '',
    avatar: ''
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_REFRESH: (state, refresh) => {
    state.refresh = refresh
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data, status } = response
        if (status < 400) {
          commit('SET_TOKEN', data.access)
          commit('SET_REFRESH', data.refresh)
          setToken(data.access)
          setRefresh(data.refresh)
        } else {
          Message.error('登录失败！用户名或密码错误。')
        }
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo().then(response => {
        const { data } = response
        if (!data) return reject('登录超时，请重新登录！')
        const { name, avatar } = data
        commit('SET_NAME', name)
        commit('SET_AVATAR', avatar)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        removeRefresh()
        removeCSRFToken()
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

