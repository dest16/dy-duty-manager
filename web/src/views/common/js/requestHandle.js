import { Message, Notification } from 'element-ui'
import { refresh } from '@/api/user'
import { setToken, getRefresh, getTokenTime } from '@/utils/auth'

/**
 * 刷新token
 */
function refreshToken() {
  // 60s内不重复刷新token
  if (Date.now() - parseFloat(getTokenTime()) > 1000 * 60) {
    const refresh_token = getRefresh()
    if (refresh_token) {
      refresh({ refresh: refresh_token }).then(result => {
        setToken(result.data.access)
      }).catch(err => {
        console.log(err)
      })
    }
  }
}

/**
 * 单个请求，请求成功后刷新token
 * @param req：function,
 * @return response
 */
async function singleRequest(req) {
  let res = null
  await req.then(result => {
    refreshToken()
    res = result
  }).catch(err => {
    console.log(err)
  })
  return res
}

/**
 * 多个请求，请求成功后刷新token
 * @param req：Array [functions]
 * @return Promise
 */
async function multipleRequests(req) {
  let res = null
  await Promise.all(req).then(result => {
    refreshToken()
    res = result
  }).catch(err => {
    console.log(err)
  })
  return res
}

/**
 * 提交数据请求处理
 * @param result：Object, 请求API后返回的结果，一般标准的是包含status和data的 { status: 200, data: [], ... }
 * @param that: Object, 当前组件的指针this，用于区别本function中的this，直接引用组建中方法和变量
 * @param formData：Object, 表单对象，主要用于请求出错时，将后端返回的key与form中item一一对应
 * @param callback：function, 回调函数
 * @param params：Objects, 回调函数的参数，以对象形式传入多个参数
 * @return null
 */
function requestHandle(result, that, formData, callback = undefined, params = {}) {
  if (!result || result.status >= 400) {
    // 若有loading，则以“服务”的方式引入的loading需要异步关闭
    if (params.loading) that.$nextTick(() => { params.loading.close() })
    // 由于result.data循环错误时可能出现代码错误，导致无法显示循环体后的消息提示，这里先弹一个保底
    const init_msg = Message({ showClose: true, message: '提交失败！请检查表单。', type: 'error' })

    let error_msg = ''
    that.errorMessages = {}
    Object.keys(result.data).forEach(key => {
      if (Object.keys(formData).includes(key)) {
        result.data[key].forEach((item, index) => {
          if (item instanceof Object) {
            Object.keys(item).forEach(son_key => {
              const total_key = key + '_' + index + '_' + son_key
              that.errorMessages[total_key] = item[son_key].join('\r')
              error_msg = that.errorMessages[total_key]
            })
          } else {
            that.errorMessages[key] = that.errorMessages[key] ? that.errorMessages[key] : '' + '\r' + item
            error_msg = that.errorMessages[key]
          }
        })
      } else {
        if (result.data[key][0] instanceof Object) {
          const any_son_key = Object.keys(result.data[key][0])[0]
          error_msg = key + ' > ' + any_son_key + ': ' + result.data[key][0][any_son_key]
        } else {
          let res_text
          if (Array.isArray(result.data[key])) res_text = result.data[key][0]
          else res_text = result.data[key]
          error_msg = res_text
        }
      }
    })
    // 顺利进行到此步，可立即关闭保底消息提示
    init_msg.close()
    const h = that.$createElement
    Message({
      showClose: true,
      type: 'error',
      message: h('p', null, [
        h('p', { style: 'color: red;margin-bottom: 10px' }, '提交失败！请检查表单，可能原因是：'),
        h('p', { style: 'color: red;font-weight: bold' }, error_msg)
      ]),
      duration: 5000
    })
  } else {
    Message({ showClose: true, message: (params.autoSave ? '自动保存' : '提交') + '成功！数据已保存。', type: 'success' })
    if (params.warnText) {
      Notification({
        title: '警告（10秒后自动关闭）',
        dangerouslyUseHTMLString: true,
        message: params.warnText,
        duration: 10000,
        type: 'warning'
      })
    }
    // 提交成功后的回调
    if (callback !== undefined) callback(params)
  }
}

/**
 * 获取数据请求处理
 * @param result：Object, 请求API后返回的结果，一般标准的是包含status和data的 { status: 200, data: [], ... }
 * @param callback：function, 回调函数
 * @param params：Objects, 回调函数的参数，以对象形式传入多个参数
 * @return null
 */
function getDataHandle(result, callback = undefined, params = {}) {
  if (!result || result.status >= 400) {
    Message({ showClose: true, message: '数据获取失败！请刷新页面后重试。', type: 'error' })
  } else {
    // 获取成功后的回调
    if (callback !== undefined) callback(result.data, params)
  }
}

/**
 * 删除数据请求处理
 * @param result：Object, 请求API后返回的结果，一般标准的是包含status和data的 { status: 200, data: [], ... }
 * @param success_text：String, 删除成功后的提示文字
 * @param callback：function, 回调函数
 * @param params：Objects, 回调函数的参数，以对象形式传入多个参数
 * @return null
 */
function deleteDataHandle(result, success_text, callback = undefined, params = {}) {
  if (!result || result.status >= 400) {
    Message({ showClose: true, message: '数据删除失败！请刷新页面后重试。', type: 'error' })
  } else {
    Message({ showClose: true, message: success_text, type: 'success', dangerouslyUseHTMLString: true })
    // 提交成功后的回调
    if (callback !== undefined) callback(params)
  }
}

export {
  refreshToken,
  singleRequest,
  multipleRequests,
  requestHandle,
  getDataHandle,
  deleteDataHandle
}
