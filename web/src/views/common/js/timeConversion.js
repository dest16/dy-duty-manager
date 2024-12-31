import moment from 'moment'

/**
 * 秒数转换为年、月、周、天、小时等
 * @param s: Number, 秒数
 * @return string: 换算后的组合unit
 */
function secondsConversion(s) {
  // 时间单位分级表
  const timeConversionList = [
    { min: 31104000, max: null, unit: '年' },
    { min: 2592000, max: 31104000, unit: '个月' },
    { min: 604800, max: 2592000, unit: '周' },
    { min: 86400, max: 604800, unit: '天' },
    { min: 3600, max: 86400, unit: '小时' },
    { min: 60, max: 3600, unit: '分钟' },
    { min: 1, max: 60, unit: '秒' }
  ]
  let result = ''
  timeConversionList.forEach(item => {
    if (s >= item.min && (s < item.max || item.max === null)) {
      const count = parseInt(s / item.min)
      result += count + item.unit
      s = s - item.min * count
    }
  })
  return result
}

/**
 * 日期时间格式化
 * @param date: String, 时间
 * @param format: String, 具体格式，遵循时间格式规则，如：'YYYY-MM-DD HH:mm:ss'
 * @return string
 */
function datetimeFormat(date, format) {
  return moment(date).format(format)
}

/**
 * 日期时间格式化
 * @param date: String, 时间（日期），或week day number
 * @param isDay: Boolean, 默认false，date此时应该是一个具体日期时间，当为true时，表示date是week day number
 * @return string: 具体星期X的汉字
 */
function getWeekday(date, isDay = false) {
  const weekArray = ['日', '一', '二', '三', '四', '五', '六']
  let day
  if (isDay) day = date
  else day = new Date(date).getDay()
  return weekArray[day]
}

export {
  secondsConversion,
  datetimeFormat,
  getWeekday
}
