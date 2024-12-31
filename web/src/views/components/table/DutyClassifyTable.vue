<template>
  <div class="app-container">
    <div style="margin-bottom: 15px;">
      <div style="display: flex;margin-bottom: 30px">
        <el-input v-model="searchData.search" placeholder="请输入关键字（支持所有非过滤字段）" class="filter-item" />
        <el-button type="primary" icon="el-icon-search" style="margin-left: 10px" @click="doSearch">搜索</el-button>
        <el-button icon="el-icon-refresh-right" @click="searchReset">重置</el-button>
      </div>
      <el-button type="success" icon="el-icon-plus" @click="actionObject('A')">新增</el-button>
      <el-button type="danger" icon="el-icon-close" :disabled="tableSelected.length <= 0" @click="batchActionObject('D')">删除</el-button>
      <el-button type="primary" icon="el-icon-download" plain :disabled="true">导出</el-button>
    </div>
    <el-table
      :data="tableData"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      empty-text="没有数据"
      @selection-change="selectionChange"
    >
      <el-table-column type="selection" align="center" width="50" fixed />
      <el-table-column type="index" align="center" label="序号" width="60" fixed>
        <template slot-scope="{ scope, $index }">
          {{ $index + 1 + (tablePage.currentPage - 1) * tablePage.pageSize }}
        </template>
      </el-table-column>
      <el-table-column label="类型名称" min-width="100" fixed prop="label" />
      <el-table-column label="基础津贴" min-width="120">
        <template slot-scope="scope">
          <span v-if="scope.row.allowance">￥ {{ scope.row.allowance }} 元/班次</span>
          <span v-else>无</span>
        </template>
      </el-table-column>
      <el-table-column label="餐饮补贴" min-width="120">
        <template slot-scope="scope">
          <span v-if="scope.row.subsidizedMeals">￥ {{ scope.row.subsidizedMeals }} 元/班次</span>
          <span v-else>无</span>
        </template>
      </el-table-column>
      <el-table-column label="仅假日班" align="center" min-width="80">
        <template slot-scope="scope">
          <i v-if="scope.row.holidayOnly" class="el-icon-success" />
          <i v-else class="el-icon-error" />
        </template>
      </el-table-column>
      <el-table-column label="假日双班" align="center" min-width="80">
        <template slot-scope="scope">
          <i v-if="scope.row.doubleShift" class="el-icon-success" />
          <i v-else class="el-icon-error" />
        </template>
      </el-table-column>
      <el-table-column label="显示顺序" min-width="80" align="center" prop="sequence" />
      <el-table-column label="渲染颜色" align="center" min-width="110">
        <template slot-scope="scope">
          <span v-if="!scope.row.color">无</span>
          <div v-else class="duty-classify-color" :style="'background:' + scope.row.color">{{ scope.row.color }}</div>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" min-width="160" prop="createTime" />
      <el-table-column label="最新修改时间" min-width="160" prop="modifyTime" />
      <el-table-column label="操作" align="center" width="160px" fixed="right">
        <template slot-scope="scope">
          <el-button-group>
            <el-button type="primary" icon="el-icon-edit" style="padding: 10px" @click="actionObject('E', scope.row)">编辑</el-button>
            <el-button type="danger" icon="el-icon-delete" style="padding: 10px" @click="actionObject('D', scope.row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <div class="table-pagination">
      <el-pagination
        :current-page="tablePage.currentPage"
        :page-sizes="[10, 20, 50, 100, 200, 500]"
        :page-size="tablePage.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="tablePage.total"
        @size-change="handlePageChange($event, 'S')"
        @current-change="handlePageChange($event, 'C')"
      />
    </div>

    <!-- 新增/编辑数据的表单 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      :close-on-press-escape="false"
      :close-on-click-modal="false"
      top="10vh"
    >
      <DutyClassifyForm
        :dialog-visible.sync="dialogVisible"
        :data="formData"
        :fetch-data="fetchData"
      />
    </el-dialog>
  </div>
</template>

<script>
import { Loading } from 'element-ui'
import { DutyClassify } from '@/api'
import { doubleConfirmBtn } from '@/views/common/js/operation'
import { getDataHandle, deleteDataHandle, singleRequest } from '@/views/common/js/requestHandle'
import DutyClassifyForm from '@/views/components/form/DutyClassifyForm'

export default {
  name: 'DutyClassifyTable',
  components: {
    DutyClassifyForm
  },
  data() {
    return {
      // table数据
      tableData: [],
      // table中被选中的项
      tableSelected: [],
      // 表格分页设置
      tablePage: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      searchData: {
        search: ''
      },
      dialogTitle: '',
      dialogVisible: false,
      formData: undefined
    }
  },
  created() {
    // 请求API数据
    this.fetchData()
  },
  methods: {
    // 获取数据
    async fetchData() {
      // 以“服务”的方式引入获取数据时的loading
      const fullLoading = Loading.service({ text: '请稍后...', background: 'rgba(0, 0, 0, 0.7)' })
      // 构造请求参数对象
      const params = {
        search: this.searchData.search,
        limit: this.tablePage.pageSize,
        offset: (this.tablePage.currentPage - 1) * this.tablePage.pageSize
      }
      // const res = await DutyClassify.getList(params)
      const res = await singleRequest(DutyClassify.getList(params))
      // 以“服务”的方式引入的需要异步关闭
      this.$nextTick(() => { fullLoading.close() })
      // 请求处理
      getDataHandle(res, this.fetchDataCallback)
    },
    // fetchData获取数据的回调
    fetchDataCallback(data) {
      this.tableData = data.results
      this.tablePage.total = data.count
    },
    // 表格分页加载
    handlePageChange(value, type) {
      if (type === 'S') {
        this.tablePage.currentPage = 1 // PageSize变了后，自动回到第一页
        this.tablePage.pageSize = value
      } else if (type === 'C') this.tablePage.currentPage = value
      this.fetchData()
    },
    // 开始搜索
    doSearch() {
      this.tablePage.currentPage = 1
      this.fetchData()
    },
    // 重置搜索条件
    searchReset() {
      this.searchData = {
        search: ''
      }
    },
    // table选中项变化时触发
    selectionChange(value) {
      this.tableSelected = value
    },
    // 操作数据表任一对象【单个】
    actionObject(action, row) {
      if (action === 'D') {
        const id = row.id
        const label = row.label
        const text = '删除后将无法恢复，确定删除「<b style="color:#ff4500">' + label + '</b>」吗？'
        doubleConfirmBtn(text, function(that) { that.deleteConfirm(id, label) }, this)
      } else {
        if (action === 'A') {
          this.formData = undefined
          this.dialogTitle = '新增【值班类型】'
        } else if (action === 'E') {
          this.formData = row
          this.dialogTitle = '编辑【值班类型】'
        }
        this.dialogVisible = true
      }
    },
    // 二次确认删除【单个】
    async deleteConfirm(id, label) {
      // 以“服务”的方式引入loading，target默认作用于body上
      const fullLoading = Loading.service({ text: '请稍后...', background: 'rgba(0, 0, 0, 0.7)' })
      const result = await singleRequest(DutyClassify.remove(id))
      // 以“服务”的方式引入的loading需要异步关闭
      this.$nextTick(() => { fullLoading.close() })
      // 请求处理
      deleteDataHandle(result, '操作成功！「<b style="color:#ff4500">' + label + '</b>」已删除。', this.fetchData)
    },
    // 操作数据表多个选中对象【批量】
    batchActionObject(action) {
      if (action === 'D') {
        const max_length = 100
        let label
        let count_label = ''
        label = this.tableSelected.map(item => item.label).join('、')
        const label_length = label.length
        if (label_length >= max_length) {
          label = label.slice(0, max_length - 3) + '...'
          count_label = '等共计 <b style="color:#d03440">' + this.tableSelected.length + '</b> 条数据'
        }
        const text = '删除后将无法恢复，确定删除「<b style="color:#ff4500">' + label + '</b>」' + count_label + '吗？'
        doubleConfirmBtn(text, function(that) { that.batchDeleteConfirm(label, count_label) }, this)
      }
    },
    // 二次确认删除【批量】
    async batchDeleteConfirm(label, count_label) {
      // 以“服务”的方式引入loading，target默认作用于body上
      const fullLoading = Loading.service({ text: '请稍后...', background: 'rgba(0, 0, 0, 0.7)' })
      const submitData = this.tableSelected.map(item => item.id) // 要删除对象的id数组
      const result = await singleRequest(DutyClassify.batchDelete(submitData))
      // 以“服务”的方式引入的loading需要异步关闭
      this.$nextTick(() => { fullLoading.close() })
      // 请求处理
      deleteDataHandle(result, '操作成功！「<b style="color:#ff4500">' + label + '</b>」' + count_label + '已删除。', this.fetchData)
    }
  }
}
</script>

<style scoped>
  ::v-deep .el-dialog {
    width: 98%;
    max-width: 750px;
  }

  [class^="el-icon-"] {
    font-size: 24px;
    vertical-align: text-top;
  }

  .el-icon-success {
    color: #67c23a;
  }

  .el-icon-error {
    color: #f56c6c;
  }

  .table-pagination {
    text-align: right;
    margin: 20px;
  }

  ::v-deep .el-select {
    width: 100%;
    max-width: 500px;
  }

  ::v-deep .el-input {
    max-width: 500px;
  }

  .filter-item+.filter-item {
    margin-left: 30px;
  }

  .duty-classify-color {
    color: rgb(255, 255, 255);
    padding: 5px 10px;
    text-align: center;
    border-radius: 5px;
  }
</style>
