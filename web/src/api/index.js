// 注册api目录，避免报错“@/api 模块不存在”
const api = {}
const exclude = ['./index.js']

// 此文件所在当前目录下递归查找.js文件
const files = require.context('.', true, /\.js$/)

files.keys().forEach(key => {
  if (!exclude.includes(key)) {
    const apiName = key.match(/\.\/(.*)\.js/)[1]
    api[apiName] = files(key)
  }
})

module.exports = api
