<template>
  <div v-loading="loading">
    <el-form ref="elForm" :model="formData" label-position="right" label-width="80px" style="width:100%; padding: 0 5%;">
      <el-form-item
        label="人员姓名"
        prop="name"
        :rules="[
          { required: true, message: '请输入值班人员的姓名', trigger: 'blur' },
          { min: 2, max: 64, message: '值班人员的姓名应为2~64个字符', trigger: 'blur' }
        ]"
      >
        <el-input v-model="formData.name" placeholder="请输入值班人员的姓名" />
      </el-form-item>
      <el-form-item
        label="联系电话"
        prop="tel"
        :rules="[
          { required: true, message: '请输入值班人员的联系电话', trigger: 'blur' },
          { min: 5, max: 16, message: '值班人员的联系电话应为5~16个字符', trigger: 'blur' }
        ]"
      >
        <el-input v-model="formData.tel" placeholder="请输入值班人员的联系电话" />
      </el-form-item>
      <el-form-item
        label="值班类型"
        prop="classify"
        :rules="{ required: true, message: '请选择至少一种值班类型' }"
      >
        <el-select v-model="formData.classify" filterable multiple placeholder="请选择值班类型">
          <el-option
            v-for="item in dutyClassifyList"
            :key="item.id"
            :label="item.label"
            :value="item.id"
          >
            <span :style="'color:' + item.color">{{ item.label }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        label="值班顺序"
        prop="sequence"
        :rules="{ required: true, message: '请输入值班顺序（越小越优先）', trigger: 'blur' }"
      >
        <el-input-number v-model="formData.sequence" :precision="0" :step="1" :min="0" />
      </el-form-item>
    </el-form>
    <div style="text-align: right">
      <el-button size="medium" icon="el-icon-circle-close" @click="$emit('update:dialogVisible', false)">取消</el-button>
      <el-button size="medium" type="success" icon="el-icon-circle-check" @click="validForm">保存</el-button>
    </div>
  </div>
</template>

<script>
import { DutyPersonnel, DutyClassify } from '@/api'
import { doubleConfirmBtn } from '@/views/common/js/operation'
import { requestHandle, singleRequest } from '@/views/common/js/requestHandle'

export default {
  name: 'DutyPersonnelForm',
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
        name: '', // 值班类型的名称，string（64）
        tel: '', // 联系电话，string（16）
        classify: [], // 值班类型，array
        sequence: 0 // 值班顺序，int
      },
      dutyClassifyList: []
    }
  },
  watch: {
    dialogVisible: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          // dialog打开时，若data未定义，则重置表单为初始化数据
          this.formData = JSON.parse(JSON.stringify(this.data === undefined ? this.initData : this.data))
          // 获取可选的值班类型数据列表
          this.getDutyClassifyList()
        } else if (!newValue) {
          // dialog关闭时，清除表单校验结果
          this.$refs.elForm.clearValidate()
          this.formData = JSON.parse(JSON.stringify(this.initData))
        }
      }
    }
  },
  methods: {
    // 获取值班类型列表，用于选择
    async getDutyClassifyList() {
      this.loading = true
      const res = await singleRequest(DutyClassify.getList({}, 'dictionary/'))
      // this.dutyClassifyList = []
      if (res.data) this.dutyClassifyList = res.data
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
          text = '正在' + text + '值班人员「<b style="color:#ff4500">' + this.formData.name + '（' + this.formData.tel + '）</b>」，确定提交吗？'
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
      if (action === 'create') result = await singleRequest(DutyPersonnel.create(this.formData))
      else result = await singleRequest(DutyPersonnel.update(this.formData.id, this.formData))
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
</style>
