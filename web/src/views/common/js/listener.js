/**
 * 事件监听器
 * @param eventList：事件列表
 * @param func：Function
 */
export function addListener(eventList = [], func) {
  /*
    mousedown: 按下鼠标时触发此事件
    mousemove: 鼠标移动时触发此事件
    keydown: 当键盘上某个按键被按下时触发此事件
    scroll: 页面滚动条位置发生变化时触发事件
   */
  eventList.forEach(e => {
    document.addEventListener(e, function() {
      func()
    })
  })
}
