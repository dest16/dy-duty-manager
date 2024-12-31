/**
 * 按钮点击后，二次确认
 * @param text：String, 二次确认提示文本
 * @param func: Function, 点击“确定”后要执行的函数
 * @param thisObj：Object, 当前DOM的指针，避免部分情况下this在js中被混淆，导致页面指针丢失
 * @return null
 */
export function doubleConfirmBtn(text, func, thisObj) {
  let that
  if (thisObj) that = thisObj
  else that = this
  that.$confirm(text, '操作确认', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    dangerouslyUseHTMLString: true,
    type: 'warning'
  }).then(() => {
    if (thisObj) func(that)
    else func()
  }).catch(() => {
    that.$message({
      showClose: true,
      type: 'info',
      message: '操作已取消'
    })
  })
}
