<template>
  <div v-loading="loading">
    <div style="font-weight: bold;font-size: 20px;text-align: center;padding: 10px">
      {{ year }}年
      <el-link
        type="primary"
        :underline="false"
        :href="`/MonthPlan?ym=${lastYM}`"
      >
        <i class="el-icon-d-arrow-left" style="font-size: 20px;line-height: 15px;" />
      </el-link>
      {{ month }}月
      <el-link
        type="primary"
        :underline="false"
        :href="`/MonthPlan?ym=${nextYM}`"
      >
        <i class="el-icon-d-arrow-right" style="font-size: 20px;line-height: 15px;" />
      </el-link>
      值班表
    </div>
    <!--
    <el-checkbox-group v-model="checkboxGroup" size="medium">
      <el-checkbox-button
        v-for="c in classData"
        :label="c[1]"
        :key="'Class_Check_' + c[0]"
      >
        {{ c[1] }}
      </el-checkbox-button>
    </el-checkbox-group>
    -->
    <div style="width: 100%;display: flex">
      <el-input
        v-model="search"
        placeholder="输入关键字搜索"
        size="small"
        prefix-icon="el-icon-search"
        clearable
      />
    </div>
    <el-table
      :data="planData.filter(item => !search || Object.values(item).join().replaceAll('-', '/').toLowerCase().includes(search.toLowerCase()))"
      stripe
      style="width: 100%"
      :max-height="height"
    >
      <el-table-column
        fixed
        align="center"
        label="日期"
        width="110"
      >
        <template slot-scope="{ row }">
          {{ datetimeFormat(row.date, 'M/D') }} 周{{ getWeekday(row.date) }}
        </template>
      </el-table-column>
      <el-table-column
        v-for="c in classData"
        :key="'Class_' + c[0]"
        align="center"
        :prop="c[0]"
        :label="c[1]"
        min-width="65"
      />
    </el-table>
  </div>
</template>

<script>
import { DutyCalendar } from '@/api'
import { getDataHandle } from '@/views/common/js/requestHandle'
import { datetimeFormat, getWeekday } from '@/views/common/js/timeConversion'

export default {
  name: 'MonthPlan',
  data() {
    return {
      loading: false,
      search: '',
      year: null,
      month: null,
      lastYM: '',
      nextYM: '',
      classData: [],
      planData: [],
      height: window.innerHeight - 43 - 32
      // checkboxGroup: []
    }
  },
  mounted() {
    window.onresize = () => {
      return (() => { this.height = window.innerHeight - 43 - 32 })()
    }
  },
  activated() {
    this.height = window.innerHeight - 43 - 32
  },
  watch: {
    '$route.query.ym': {
      immediate: true,
      handler(newValue) {
        this.getWholeMonthPlan(newValue)
      }
    }
  },
  methods: {
    datetimeFormat,
    getWeekday,
    async getWholeMonthPlan(ym) {
      this.loading = true
      if(!ym) ym = datetimeFormat(new Date(), 'YYYY-MM')
      const y_m = ym.split('-')
      this.year = Number(y_m[0])
      this.month = Number(y_m[1])

      // 计算上一个月、下一个月
      if (this.month === 1) {
        this.lastYM = (this.year - 1) + '-12'
        this.nextYM = this.year + '-02'
      } else if (this.month === 12) {
        this.lastYM = this.year + '-11'
        this.nextYM = (this.year + 1) + '-01'
      } else {
        const lastM = this.month - 1
        const nextM = this.month + 1
        this.lastYM = this.year + '-' + (lastM >= 10 ? lastM : '0' + lastM)
        this.nextYM = this.year + '-' + (nextM >= 10 ? nextM : '0' + nextM)
      }
      console.log(this.lastYM, this.nextYM)
      const res = await DutyCalendar.getWholeMonthPlan({ ym: ym })
      getDataHandle(res, this.getWholeMonthPlanCallback)
      this.loading = false
    },
    getWholeMonthPlanCallback(data) {
      this.classData = data.class
      this.planData = data.plan
    }
  }
}
</script>

<style scoped lang="scss">
  ::v-deep .el-input {
    width: 60%;
    margin: auto;

    input {
      text-align: center;
      border-radius: 50px;
    }
  }
</style>
