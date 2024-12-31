<template>
  <div v-loading="loading">
    <el-form ref="elForm" :model="formData" label-position="right" label-width="80px" style="width:100%;padding: 0 10px">
      <el-form-item label="日期" prop="date" :rules="{ required: true, message: '请选择日期' }">
        <el-date-picker
          v-model="formData.date"
          type="date"
          placeholder="请选择日期"
          format="yyyy年M月d日"
          value-format="yyyy-MM-dd"
        />
      </el-form-item>
      <el-form-item label="假日名称" prop="name" :rules="{ required: true, message: '请选择假日名称' }">
        <el-select v-model="formData.name" filterable allow-create placeholder="请选择假日名称">
          <el-option v-for="hn in holidayNameList" :key="'hn' + hn" :label="hn" :value="hn" />
        </el-select>
      </el-form-item>
      <el-row v-for="(dc, index) in formData.festival_plan" :key="'dc' + dc.classify + dc.id">
        <el-form-item v-if="dutyClassifyDict[dc.classify]" :label="dutyClassifyDict[dc.classify].label" required>
          <el-col v-if="dutyClassifyDict[dc.classify].allowance > 0" :span="10">
            <el-form-item label="" label-width="0" :prop="'festival_plan.' + index + '.allowanceMultiple'" :style="'color:' + dutyClassifyDict[dc.classify].color">
              <span class="duty-classify-label" :style="'background:' + dutyClassifyDict[dc.classify].color">基本津贴</span>
              <span>{{ dutyClassifyDict[dc.classify].allowance }} × </span>
              <el-input-number
                v-model="dc.allowanceMultiple"
                controls-position="right"
                :precision="2"
                :step="1"
                :min="1"
                :max="10"
                class="width-100-ein"
              />
            </el-form-item>
          </el-col>
          <el-col v-if="dutyClassifyDict[dc.classify].subsidizedMeals > 0" :span="10">
            <el-form-item label="" label-width="0" :prop="'festival_plan.' + index + '.subsidizedMealsMultiple'" :style="'margin-left:15px;color:' + dutyClassifyDict[dc.classify].color">
              <span class="duty-classify-label" :style="'background:' + dutyClassifyDict[dc.classify].color">餐饮补贴</span>
              <span>{{ dutyClassifyDict[dc.classify].subsidizedMeals }} × </span>
              <el-input-number
                v-model="dc.subsidizedMealsMultiple"
                controls-position="right"
                :precision="2"
                :step="1"
                :min="1"
                :max="10"
                class="width-100-ein"
              />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label-width="0">
              <span class="estimate-cost" v-html="estimateCost(dc)" />
            </el-form-item>
          </el-col>
        </el-form-item>
      </el-row>
    </el-form>
    <div style="text-align: right">
      <el-button size="medium" icon="el-icon-circle-close" @click="$emit('update:dialogVisible', false)">取消</el-button>
      <el-button size="medium" type="success" icon="el-icon-circle-check" @click="validForm">保存</el-button>
    </div>
  </div>
</template>

<script>
import { DutyClassify, HolidaysAndFestivals } from '@/api'
import { doubleConfirmBtn } from '@/views/common/js/operation'
import { requestHandle, singleRequest } from '@/views/common/js/requestHandle'
import { ArrayToDictionary, RetainTheDecimal } from '@/views/common/js/dataConversion'

export default {
  name: 'HolidaysAndFestivals',
  props: {
    // 外层dialogVisible控制
    dialogVisible: {
      type: Boolean,
      default: false
    },
    // 表单数据
    data: undefined,
    // table刷新方法
    fetchData: {
      type: Function,
      default: null
    }
  },
  data() {
    return {
      loading: false,
      formData: {},
      initData: {
        date: '', // 日期，string（$date）
        name: '', // 假日名称，string（64）
        festival_plan: [] // 假日加倍计划
      },
      // 值班类型数据列表
      dutyClassifyList: [],
      dutyClassifyDict: {},
      holidayNameList: [
        '元旦节（当天）', '元旦节（假期）',
        '除夕',
        '春节（当天）', '春节（假期）',
        '清明节（当天）', '清明节（假期）',
        '劳动节（当天）', '劳动节（假期）',
        '端午节（当天）', '端午节（假期）',
        '中秋节（当天）', '中秋节（假期）',
        '国庆节（当天）', '国庆节（假期）'
      ]
    }
  },
  watch: {
    dialogVisible: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          // dialog打开时，若data未定义，则重置表单为初始化数据
          this.formData = JSON.parse(JSON.stringify(this.data === undefined ? this.initData : this.data))
          // 获取值班类型列表，用于初始化表单
          this.getDutyClassifyList()
        } else {
          // dialog关闭时，清除表单校验结果
          this.$refs.elForm.clearValidate()
          this.formData = JSON.parse(JSON.stringify(this.initData))
        }
      }
    }
  },
  methods: {
    // 计算预估津贴、补贴总费用
    estimateCost(dc) {
      const dc_details = this.dutyClassifyDict[dc.classify]
      const allowance = dc_details.allowance
      const subsidizedMeals = dc_details.subsidizedMeals
      const allowanceMultiple = dc.allowanceMultiple
      const subsidizedMealsMultiple = dc.subsidizedMealsMultiple
      dc.totalAllowance = allowance * allowanceMultiple
      dc.totalSubsidizedMeals = subsidizedMeals * subsidizedMealsMultiple
      let sum = dc.totalAllowance + dc.totalSubsidizedMeals
      if (sum > 0) {
        sum = '<em style="font-weight: bold;color: #F56C6C">' + RetainTheDecimal(sum, 2) + '</em>'
        return '合计￥' + sum + '元'
      } else return ''
    },
    // 获取值班类型列表，用于初始化表单
    async getDutyClassifyList() {
      this.loading = true
      const res = await singleRequest(DutyClassify.getList({}, 'dictionary/'))
      if (res.data) {
        this.dutyClassifyList = res.data
        this.dutyClassifyDict = ArrayToDictionary(res.data, 'id')
        if (!this.formData.id) {
          // 如果formData的id不存在，则表示是“新增”，要从值班类型获取不同类型的津贴、餐补初始值，并初始化到当前formData中
          const festival_plan = []
          this.dutyClassifyList.forEach(item => {
            // 当前仅当allowance和subsidizedMeals之和大于0时，才有意义，允许渲染
            if (item.allowance + item.subsidizedMeals > 0) {
              festival_plan.push(
                {
                  classify: item.id,
                  allowanceMultiple: 1.0,
                  totalAllowance: 0.0,
                  subsidizedMealsMultiple: 1.0,
                  totalSubsidizedMeals: 0.0
                }
              )
            }
          })
          this.formData.festival_plan = festival_plan
        }
      }
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
          text = '正在' + text + '假日「<b style="color:#ff4500">' + this.formData.date + '，' + this.formData.name + '</b>」，确定提交吗？'
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
      const submitData = JSON.parse(JSON.stringify(this.formData))
      let result
      if (action === 'create') result = await singleRequest(HolidaysAndFestivals.create(submitData))
      else result = await singleRequest(HolidaysAndFestivals.update(submitData.id, submitData))
      this.loading = false
      // 请求处理
      requestHandle(result, this, submitData, this.successCallBack)
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

  .date-details-text {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 30px;
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

  .duty-classify-label {
    color: #fff;
    padding: 8px 10px 8px 8px;
    border-bottom-right-radius: 25px;
    border-top-right-radius: 25px;
    margin-right: 5px;
    font-size: 12px;
    vertical-align: bottom;
  }
</style>
