/**
 * 数组转字典
 * @param list：Array, 字典元素的数组数据
 * @param key: String, 转为字典后，用于做key的属性名称
 * @param delKey：String
 *        默认为 ''，即自动从value中剔除当前key，例如，key = 'date'，[{ name: 'xxx', date: '20210101' }, ...] ==> { 20210101: { name: 'xxx' }, ...}
 *        当传入值为 false 时，则完全转换，例如，key = 'date'，[{ name: 'xxx', date: '20210101' }, ...] ==> { 20210101: { name: 'xxx', date: '20210101' }, ...}
 *        当传入值为具体属性名时，视为仅保留传入属性名的值，例如，key = 'date'、delKey = 'name'，[{ name: 'xxx', date: '20210101' }, ...] ==> { 20210101: 'xxx', ...}
 * @return Object(dict)
 */
export function ArrayToDictionary(list, key, delKey = '') {
  const dict = {}
  // 必须完全拷贝原list，否则会直接修改list的属性值
  const new_list = JSON.parse(JSON.stringify(list))
  new_list.forEach(item => {
    const k = item[key]
    if (delKey === '') {
      delete item[key]
      dict[k] = item
    } else if (delKey === false) {
      dict[k] = item
    } else {
      dict[k] = item[delKey]
    }
  })
  return dict
}

/**
 * 四舍五入保留指定位数小数
 * @param num：Float, 要处理的数字
 * @param dig: Int, 默认两位，要保留的小数位
 * @param bank：Boolean, 是否按照银行的“四舍六入五取偶”进行计算，默认false
 *        若为true，四舍六入五考虑，五后非零就进一，五后为零看奇偶，五前为偶应舍去，五前为奇要进一
 *        若为false，四舍五入，与数学中的四舍五入完全一致
 * @return number
 */
export function RetainTheDecimal(num, dig = 2, bank = false) {
  if (bank === true) return parseFloat(num.toFixed(dig))
  else {
    let result = parseFloat(num)
    if (isNaN(result)) return num
    const mul = Math.pow(10, dig)
    result = Math.round(num * mul) / mul
    let s_x = result.toString()
    let pos_decimal = s_x.indexOf('.')
    if (pos_decimal < 0) {
      pos_decimal = s_x.length
      s_x += '.'
    }
    while (s_x.length <= pos_decimal + dig) {
      s_x += '0'
    }
    return parseFloat(s_x)
  }
}
