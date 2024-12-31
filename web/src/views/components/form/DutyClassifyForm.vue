<template>
  <div v-loading="loading">
    <el-form ref="elForm" :model="formData" label-position="right" label-width="80px" style="width:100%; padding: 0 5%;">
      <el-form-item
        label="类型名称"
        prop="label"
        :rules="[
          { required: true, message: '请输入值班类型的名称', trigger: 'blur' },
          { min: 1, max: 16, message: '值班类型的名称不超过16个字符', trigger: 'blur' }
        ]"
      >
        <el-input v-model="formData.label" placeholder="请输入值班类型的名称" />
      </el-form-item>
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="基础津贴"
            prop="allowance"
            :rules="{ required: true, message: '请输入当前值班类型的基础津贴', trigger: 'blur' }"
          >
            ￥ <el-input-number v-model="formData.allowance" :step="100" :min="0" :max="1000" /> 元/班次
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
        label="餐饮补贴"
        prop="subsidizedMeals"
        :rules="{ required: true, message: '请输入当前值班类型的餐饮补贴', trigger: 'blur' }"
      >
        ￥ <el-input-number v-model="formData.subsidizedMeals" :step="10" :min="0" :max="100" /> 元/班次
      </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="仅假日班" prop="holidayOnly" required>
            <el-switch v-model="formData.holidayOnly" active-color="#13ce66" />
            <span class="el-input-question" style="padding: 0 20px">
              <el-tooltip
                effect="dark"
                content="“仅假日班”即只有节假日时才值的班。例如白班。"
                placement="top"
              >
                <i class="el-icon-warning" />
              </el-tooltip>
            </span>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="假日双班" prop="doubleShift" required>
        <el-switch v-model="formData.doubleShift" active-color="#13ce66" />
        <span class="el-input-question" style="padding: 0 20px">
          <el-tooltip
            effect="dark"
            content="“假日双班”即节假日时为双班制，即使同一个人值班，自动算两个班次。例如周末的应用值班。"
            placement="top"
          >
            <i class="el-icon-warning" />
          </el-tooltip>
        </span>
      </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="显示顺序"
            prop="sequence"
            :rules="{ required: true, message: '请输入显示顺序（越小越优先）', trigger: 'blur' }"
          >
            <el-input-number v-model="formData.sequence" :precision="0" :step="1" :min="0" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="渲染颜色" prop="color">
            <el-color-picker
              v-model="formData.color"
              :predefine="['#ff4500', '#ff8c00', '#ffd700', '#90ee90', '#00ced1', '#1e90ff', '#c71585']"
            />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div style="text-align: right">
      <el-button size="medium" icon="el-icon-circle-close" @click="$emit('update:dialogVisible', false)">取消</el-button>
      <el-button size="medium" type="success" icon="el-icon-circle-check" @click="validForm">保存</el-button>
    </div>
  </div>
</template>

<script>
import { DutyClassify } from '@/api'
import { doubleConfirmBtn } from '@/views/common/js/operation'
import { requestHandle, singleRequest } from '@/views/common/js/requestHandle'

export default {
  name: 'DutyClassifyForm',
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
        label: '', // 值班类型的名称，string（16）
        allowance: 0.00, // 值班的基础津贴，float（16），值在0~1000之间,
        subsidizedMeals: 0.00, // 值班的餐饮补贴，float（16），值在0~1000之间,
        holidayOnly: false, // 仅假日班（只有假日才值的班，默认false），boolean
        doubleShift: false, // 假日双班（假日是否记作两个班次，默认false），boolean
        sequence: 0, // 显示顺序，默认0，正序排列
        color: '#000000' // 值班类型的渲染颜色，string（32）
      }
    }
  },
  watch: {
    dialogVisible: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          // dialog打开时，若data未定义，则重置表单为初始化数据
          this.formData = JSON.parse(JSON.stringify(this.data === undefined ? this.initData : this.data))
        } else if (!newValue) {
          // dialog关闭时，清除表单校验结果
          this.$refs.elForm.clearValidate()
          this.formData = JSON.parse(JSON.stringify(this.initData))
        }
      }
    }
  },
  methods: {
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
          text = '正在' + text + '值班类型「<b style="color:#ff4500">' + this.formData.label + '</b>」，确定提交吗？'
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
      let result
      if (action === 'create') result = await singleRequest(DutyClassify.create(this.formData))
      else result = await singleRequest(DutyClassify.update(this.formData.id, this.formData))
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
      vertical-align: middle;
    }
  }

  ::v-deep .el-color-picker__trigger {
    width: 100px;
  }

  ::v-deep .el-input-number {
    width: 150px;
  }
</style>
