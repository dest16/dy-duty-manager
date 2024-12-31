<template>
  <div v-loading="loading">
    <el-form ref="elForm" :model="formData" label-position="right" label-width="80px" style="width:100%;padding: 0 10px;">
      <div class="date-details-text">
        <span>{{ datetimeFormat(formData.date, 'YYYY年M月D日') }}</span>
        <span style="margin-left: 20px">周{{ getWeekday(formData.date) }}</span>
        <span style="margin-left: 20px">{{ formData.holiday ? '休假日' : '工作日' }}</span>
      </div>
      <div v-if="isFestivals || isPublicHoliday" style="text-align: center">
        <svg-icon icon-class="festivals" class-name="festivals-svg-icon" />
        <svg-icon icon-class="festivals" class-name="festivals-svg-icon" />
        <svg-icon icon-class="festivals" class-name="festivals-svg-icon" />
        <span class="festivals-name">{{ holidaysAndFestivals.name || '周末' }}</span>
        <svg-icon icon-class="festivals" class-name="festivals-svg-icon" />
        <svg-icon icon-class="festivals" class-name="festivals-svg-icon" />
        <svg-icon icon-class="festivals" class-name="festivals-svg-icon" />
      </div>
      <el-form-item v-if="formData.holiday || isFestivals || isPublicHoliday" label="是否假日" prop="holiday">
        <el-switch v-model="formData.holiday" @change="changeHoliday" />
      </el-form-item>
      <div v-else style="margin-bottom: 20px;">
        <el-alert title="当前日期为工作日，若需设置为假日，请到“假日管理”中添加" type="warning" show-icon :closable="false" center />
      </div>

      <el-row v-for="(dc, index) in formData.calendar_plan" :key="'dc' + dc.classify + dc.id">
        <div v-if="dutyClassifyDict[dc.classify] && (!dutyClassifyDict[dc.classify].holidayOnly || formData.holiday)">
          <el-col :span="9">
            <el-form-item
              :label="dutyClassifyDict[dc.classify].label"
              :prop="'calendar_plan.' + index + '.personnel'"
              :rules="{ required: true, message: '请选择' + dutyClassifyDict[dc.classify].label + '人员' }"
            >
              <span class="el-select-left" :style="'border-left-color:' + dutyClassifyDict[dc.classify].color" />
              <el-select v-model="dc.personnel" filterable placeholder="请选择值班人员">
                <el-option
                  v-for="dp in dutyPersonnelClassify[dc.classify]"
                  :key="'dp_' + dc.classify + dp.id"
                  :label="dpLabel(dp)"
                  :value="dp.id"
                />
              </el-select>
              <el-link
                v-if="dutyPersonnelDict[dc.personnel] && dutyPersonnelDict[dc.personnel].tel"
                :href="'tel:' + dutyPersonnelDict[dc.personnel].tel"
                :underline="false"
                class="contact-duty-person"
              >
                <svg-icon icon-class="tel" />
              </el-link>
            </el-form-item>
          </el-col>
          <el-col v-if="dutyClassifyDict[dc.classify].allowance > 0" :span="6">
            <el-form-item label="津贴" label-width="60px" :prop="'calendar_plan.' + index + '.totalAllowance'">
              <el-input-number
                v-model="dc.totalAllowance"
                controls-position="right"
                :step="dutyClassifyDict[dc.classify].allowance"
                :min="0"
                :max="dutyClassifyDict[dc.classify].allowance * 10"
                class="width-100-ein"
              />
            </el-form-item>
          </el-col>
          <el-col v-if="dutyClassifyDict[dc.classify].subsidizedMeals > 0" :span="6">
            <el-form-item label="餐补" label-width="60px" :prop="'calendar_plan.' + index + '.totalSubsidizedMeals'">
              <el-input-number
                v-model="dc.totalSubsidizedMeals"
                controls-position="right"
                :step="dutyClassifyDict[dc.classify].subsidizedMeals"
                :min="0"
                :max="dutyClassifyDict[dc.classify].subsidizedMeals * 10"
                class="width-100-ein"
              />
            </el-form-item>
          </el-col>
          <el-col :span="3">
            <el-form-item label-width="0">
              <span class="estimate-cost" v-html="estimateCost(dc)" />
            </el-form-item>
          </el-col>
        </div>
      </el-row>
    </el-form>
    <div style="text-align: right">
      <el-button size="medium" icon="el-icon-circle-close" @click="$emit('update:dialogVisible', false)">取消</el-button>
      <el-button v-if="formData.id" size="medium" type="danger" icon="el-icon-delete" @click="beforeDeleteObject">删除</el-button>
      <el-button size="medium" type="success" icon="el-icon-circle-check" @click="validForm">保存</el-button>
    </div>
  </div>
</template>

<script>
import { DutyPersonnel, DutyClassify, DutyCalendar, HolidaysAndFestivals } from '@/api'
import { doubleConfirmBtn } from '@/views/common/js/operation'
import { deleteDataHandle, requestHandle, singleRequest, multipleRequests } from '@/views/common/js/requestHandle'
import { RetainTheDecimal, ArrayToDictionary } from '@/views/common/js/dataConversion'
import { datetimeFormat, getWeekday } from '@/views/common/js/timeConversion'

export default {
  name: 'DutyCalendarForm',
  props: {
    // 外层dialogVisible控制
    dialogVisible: {
      type: Boolean,
      default: false
    },
    // 表单数据
    data: undefined,
    // 当前点击的日期
    date: {
      type: String,
      default: ''
    },
    // table刷新方法
    fetchData: {
      type: Function,
      default: null
    }
  },
  data() {
    return {
      loading: false,
      publicHoliday: ['六', '日'], // 周末一般算假日，除非调休导致变成工作日
      formData: {},
      initData: {
        date: '', // 日期，string（$date）
        holiday: false, // 是否是假日，默认不是假日（包括节假日、休假日），一般情况下周末会被自动识别为假日
        festival: null, // 节日（从“假日管理”中添加的节日选取）
        calendar_plan: [] // 排班计划
      },
      // 值班人员按值班类型分类
      dutyPersonnelClassify: {},
      // 值班人员字典（以id为key）
      dutyPersonnelDict: {},
      // 值班类型数据列表
      dutyClassifyList: [],
      // 值班类型数据字典
      dutyClassifyDict: {},
      // 当天日期对应的节日、假日数据
      holidaysAndFestivals: {}
    }
  },
  computed: {
    isPublicHoliday() {
      // 周末一般算假日，除非调休导致变成工作日
      const publicHoliday = ['六', '日']
      return publicHoliday.includes(getWeekday(this.formData.date))
    },
    isFestivals() {
      return !!this.holidaysAndFestivals.date
    }
  },
  watch: {
    dialogVisible: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          // dialog打开时，若data未定义，则重置表单为初始化数据
          this.initData.date = this.date
          this.formData = JSON.parse(JSON.stringify(this.data === undefined ? this.initData : this.data))
          // 获取可选的值班人员数据列表
          this.getDutyPersonnelList()
        } else {
          // dialog关闭时，清除表单校验结果
          this.$refs.elForm.clearValidate()
          this.formData = JSON.parse(JSON.stringify(this.initData))
        }
      }
    }
  },
  methods: {
    datetimeFormat,
    getWeekday,
    // 格式化选择人员时的label显示
    dpLabel(dp) {
      return dp.tel ? dp.name + '（' + dp.tel + '）' : dp.name
    },
    // 是否假日改变时的动作
    changeHoliday(value) {
      // 将当前日期的假日加倍计划转化为字典，方便一一对应
      let hf_dict
      if (this.isFestivals) hf_dict = ArrayToDictionary(this.holidaysAndFestivals.festival_plan, 'classify')
      this.formData.calendar_plan.forEach(item => {
        let hf_plan
        // 如果是假日，且是节日
        if (this.isFestivals) hf_plan = hf_dict[item.classify]
        if (!hf_plan) hf_plan = { allowanceMultiple: 1, subsidizedMealsMultiple: 1 }
        // 如果“假日双班”为True，则所有费用均乘以2
        const double_shift = this.dutyClassifyDict[item.classify].doubleShift ? 2 : 1
        if (value) {
          item.totalAllowance *= hf_plan.allowanceMultiple * double_shift
          item.totalSubsidizedMeals *= hf_plan.subsidizedMealsMultiple * double_shift
        } else {
          item.totalAllowance = RetainTheDecimal(item.totalAllowance / hf_plan.allowanceMultiple / double_shift, 0)
          item.totalSubsidizedMeals = RetainTheDecimal(item.totalSubsidizedMeals / hf_plan.subsidizedMealsMultiple / double_shift, 0)
          // 如果不是假日，则“仅假日班”为True的人员信息要清空，；主要是为了后端存储的数据不出现多余的，避免统计时出差错
          if (this.dutyClassifyDict[item.classify].holidayOnly) item.personnel = null
        }
      })
      // 如果是假日，那么检查holidaysAndFestivals是否获取到假日数据，否则自动变为不是假日
      if (value) {
        if (!this.isPublicHoliday && !this.isFestivals) {
          this.$message({
            showClose: true,
            type: 'error',
            message: '当前日期既非周末，也未查询到节日信息，不允许设置为假日。'
          })
          this.formData.holiday = false
        }
      } else {
        // 若非假日，清空festival
        this.formData.festival = null
      }
    },
    // 计算预估津贴、补贴总费用
    estimateCost(obj) {
      let sum = obj.totalAllowance + obj.totalSubsidizedMeals
      if (sum > 0) {
        sum = '<em style="font-weight: bold;color: #F56C6C">' + RetainTheDecimal(sum, 0) + '</em>'
        return '合计￥' + sum + '元'
      } else return ''
    },
    // 获取值班人员列表，用于选择
    async getDutyPersonnelList() {
      this.loading = true
      // const allRes = await Promise.all([
      //   DutyClassify.getList({}, 'dictionary/'), // 获取值班类型列表，用于展示预估津贴、补贴
      //   DutyPersonnel.getList({}, 'dictionary/'), // 获取值班人员列表
      //   HolidaysAndFestivals.getList({ date: this.formData.date }, 'getHFDateDetail/') // 获取当天日期对应的节日、假日
      // ])
      const allRes = await multipleRequests([
        DutyClassify.getList({}, 'dictionary/'), // 获取值班类型列表，用于展示预估津贴、补贴
        DutyPersonnel.getList({}, 'dictionary/'), // 获取值班人员列表
        HolidaysAndFestivals.getList({ date: this.formData.date }, 'getHFDateDetail/') // 获取当天日期对应的节日、假日
      ])
      // 把值班类型赋值
      if (allRes[0].data) {
        this.dutyClassifyList = allRes[0].data
        this.dutyClassifyDict = ArrayToDictionary(this.dutyClassifyList, 'id')
        // 如果formData的id不存在，则表示是“新增”，要从值班类型获取不同类型的津贴、餐补初始值，并初始化到当前formData中
        if (!this.formData.id) {
          const calendar_plan = []
          this.dutyClassifyList.forEach(item => {
            calendar_plan.push(
              {
                classify: item.id,
                personnel: null,
                totalAllowance: item.allowance,
                totalSubsidizedMeals: item.subsidizedMeals
              }
            )
          })
          this.formData.calendar_plan = calendar_plan
        }
      }
      if (allRes[1].data) {
        // 把值班人员按不同值班类型划分不同列表供选择
        this.dutyPersonnelDict = ArrayToDictionary(allRes[1].data, 'id')
        // 用push追加的，必须先清空已有列表
        this.dutyPersonnelClassify = {}
        allRes[1].data.forEach(item => {
          if (this.dutyPersonnelClassify[item.classify] === undefined) {
            this.dutyPersonnelClassify[item.classify] = [item]
          } else {
            this.dutyPersonnelClassify[item.classify].push(item)
          }
        })
      }
      // 获取节日、假日的数据列表
      this.holidaysAndFestivals = {}
      if (allRes[2].data) this.holidaysAndFestivals = allRes[2].data
      // 上述数据都处理完毕后，若当前为【新增】，则初始化表单数据
      if (!this.formData.id && (this.isFestivals || this.isPublicHoliday)) {
        if (this.isFestivals) this.formData.festival = this.holidaysAndFestivals.id
        this.formData.holiday = true
        this.changeHoliday(this.formData.holiday)
      }
      this.loading = false
    },
    // 删除对象前二次确认
    beforeDeleteObject() {
      const id = this.formData.id
      const label = this.formData.date
      const text = '删除后将无法恢复，确定删除「<b style="color:#ff4500">' + label + '</b>」吗？'
      doubleConfirmBtn(text, function(that) { that.deleteConfirm(id, label) }, this)
    },
    // 删除当前对象
    async deleteConfirm(id, label) {
      this.loading = true
      const result = await singleRequest(DutyCalendar.remove(id))
      // 请求处理
      deleteDataHandle(result, '操作成功！「<b style="color:#ff4500">' + label + '</b>」已删除。', this.successCallBack)
      this.loading = false
    },
    // 验证表单全部有规则项
    validForm(text = '', fields = []) {
      // 请求API之前，先校验表单；校验通过则请求API，提交数据
      this.$refs.elForm.validate((state, obj) => {
        if (state) {
          let action
          if (this.formData.id) {
            text = '<b style="color: #FF9800">修改</b>'
            action = 'update'
          } else {
            text = '<b style="color: #0fa915">创建</b>新的'
            action = 'create'
          }
          text = '正在' + text + '值班计划「<b style="color:#ff4500">' + this.formData.date + '</b>」，确定提交吗？'
          doubleConfirmBtn(text, function(that) { that.submitForm(action) }, this)
        } else {
          // 选取obj的第一个元素error信息展示给用户
          const error_info = obj[Object.keys(obj)[0]].map(item => item.message).join('\n')
          this.$alert(error_info, '数据提交失败', {
            confirmButtonText: '确 定',
            type: 'error'
          })
        }
      })
    },
    // 提交表单
    async submitForm(action) {
      this.loading = true
      // 数据库中部分字段不允许为空，当白班为空时，要过滤掉，不传给后端
      const submitData = JSON.parse(JSON.stringify(this.formData))
      submitData.calendar_plan = submitData.calendar_plan.filter(item => !!item.personnel)
      let result
      if (action === 'create') result = await singleRequest(DutyCalendar.create(submitData))
      else result = await singleRequest(DutyCalendar.update(submitData.id, submitData))
      this.loading = false
      // 请求处理
      requestHandle(result, this, this.formData, this.successCallBack)
    },
    // 数据提交成功的回调
    successCallBack() {
      // 关闭表单窗口
      this.$emit('update:dialogVisible', false)
      // 刷新table数据
      this.fetchData()
    }
  }
}
</script>

<style scoped lang="scss">
  ::v-deep .el-input-question {
    .el-input__inner {
      border-top-right-radius: 4px;
      border-bottom-right-radius: 4px;
    }

    .el-input-group__append, .el-input-group__prepend {
      border: 0;
      background-color: unset;
    }

    [class*=" el-icon-"], [class^=el-icon-] {
      font-size: 24px;
      color: #ffa500;
    }
  }

  .estimate-cost {
    margin-left: 10px;
    font-size: 12px;
  }

  .width-100-ein {
    width: 100px;
  }

  ::v-deep .el-select .el-input__inner {
    width: 150px;
  }

  .date-details-text {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 15px;
  }

  .el-select-left {
    top: 0;
    left: 0;
    border-left: 6px solid;
    padding: 20px 0;
    z-index: 1;
    position: absolute;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
  }

  .festivals-name {
    margin: 0 10px;
    font-size: 24px;
    font-weight: bold;
    font-family: '华文行楷';
    color: #f71c66;
    vertical-align: middle;
  }

  .festivals-svg-icon {
    font-size: 36px;
    vertical-align: middle;
  }

  .contact-duty-person {
    position: absolute;
    font-size: 24px;
    color: #1fadd3;
    top: 0;
    margin-left: 5px;
  }
</style>
