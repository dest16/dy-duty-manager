<template>
  <div>
    <div style="margin: 20px;overflow: auto;position: relative">
      <div style="position: absolute;left: 200px;top: 15px;z-index: 1">
        <el-switch v-model="myself" active-color="#13ce66" active-text="只看自己" />
      </div>
      <el-calendar v-model="value" v-loading="loading">
        <template
          slot="dateCell"
          slot-scope="{ date, data }"
        >
          <div
            class="calendar-custom-grid"
            :style="isUser(data.day) ? 'background: #ffead5' : ''"
            @click="actionObject(data)"
          >
            <div class="grid-item">
              <!-- 是否节假日判断，渲染不同的UI -->
              <div v-if="dutyCalendarDict[data.day]">
                <span v-if="dutyCalendarDict[data.day].holiday" class="day-off-icon" style="background: #0fa915">休</span>
                <span
                  v-else-if="isPublicHoliday(data.day) || holidaysAndFestivalsDict[data.day]"
                  class="day-off-icon"
                  style="background: #ff6060"
                >班</span>
              </div>
              <div v-else>
                <span v-if="isPublicHoliday(data.day) || holidaysAndFestivalsDict[data.day]" class="day-off-icon" style="background: #0fa915">休</span>
              </div>
              <div
                v-if="holidaysAndFestivalsDict[data.day]"
                class="holidays-festivals-name"
                :style="'background:' + (dutyCalendarDict[data.day] && dutyCalendarDict[data.day].holiday ? '#0fa915' : '#ff6060')"
              >
                {{ holidaysAndFestivalsDict[data.day].name }}
                <span class="beautify-angle-icon" :style="'border-color:' + (dutyCalendarDict[data.day] && dutyCalendarDict[data.day].holiday ? '#0fa915' : '#ff6060')" />
              </div>
              <div :class="'date-number ' + (data.isSelected ? 'is-selected' : '')">
                {{ date.getDate() }}
              </div>
              <!-- 渲染值班详细计划 -->
              <div v-if="dutyCalendarDict[data.day]">
                <div
                  v-for="p in dutyCalendarDict[data.day].calendar_plan.filter(plan => dutyClassifyDict[plan.classify].sequence <= dutyClassifyDivide)"
                  :key="'plan_left_' + data.day + p.id"
                  class="department-person-item"
                >
                  <div v-show="(myself && p.personnel === userUUID) || !myself">
                    <span
                      class="department-label"
                      :style="'background:' + dutyClassifyDict[p.classify].color"
                    >{{ dutyClassifyDict[p.classify].label.slice(0, 1) }}</span>
                    <span
                      class="person-name key-personnel"
                      :style="'color:' + dutyClassifyDict[p.classify].color"
                    >{{ getPersonnelName(p.personnel) }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="dutyCalendarDict[data.day]" class="grid-item">
              <div
                v-for="p in dutyCalendarDict[data.day].calendar_plan.filter(plan => dutyClassifyDict[plan.classify].sequence > dutyClassifyDivide)"
                :key="'plan_right' + data.day + p.id"
                class="department-person-item"
              >
                <div v-show="(myself && p.personnel === userUUID) || !myself">
                  <span
                    class="department-label"
                    :style="'background:' + dutyClassifyDict[p.classify].color"
                  >{{ dutyClassifyDict[p.classify].label.slice(0, 1) }}</span>
                  <span
                    class="person-name key-personnel"
                    :style="'color:' + dutyClassifyDict[p.classify].color"
                  >{{ getPersonnelName(p.personnel) }}</span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </el-calendar>
    </div>
    <div>
      <!-- 新增/编辑数据的表单 -->
      <el-dialog
        :title="dialogTitle"
        :visible.sync="dialogVisible"
        :close-on-press-escape="false"
        :close-on-click-modal="false"
        top="10vh"
      >
        <DutyCalendarForm
          :dialog-visible.sync="dialogVisible"
          :data="formData"
          :date="currDate"
          :fetch-data="fetchData"
        />
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { DutyCalendar, DutyClassify, DutyPersonnel, HolidaysAndFestivals } from '@/api'
import { ArrayToDictionary } from '@/views/common/js/dataConversion'
import DutyCalendarForm from '@/views/components/form/DutyCalendarForm'
import { datetimeFormat, getWeekday } from '@/views/common/js/timeConversion'
import { multipleRequests } from '@/views/common/js/requestHandle'

export default {
  name: 'DutyCalendar',
  components: {
    DutyCalendarForm
  },
  data() {
    return {
      value: new Date(),
      loading: false,
      dialogTitle: '',
      dialogVisible: false,
      formData: undefined,
      currDate: '',
      dutyCalendarDict: {},
      dutyClassifyDict: {},
      dutyPersonnelDict: {},
      holidaysAndFestivalsDict: {},
      // 值班类型的分界（显示顺序）值，主要用于UI布局
      dutyClassifyDivide: 2,
      // 模拟当前用户uuid，用于高亮显示当前用户需要值班的日期
      userUUID: '48fa6ff0-04bb-11ec-9f9c-f4b52024bb83',
      // 模拟获取用户设置【只看自己】
      myself: false
    }
  },
  computed: {
    getPersonnelName() {
      return (pid) => {
        try {
          return this.dutyPersonnelDict[pid].name
        } catch (e) {
          return '无'
        }
      }
    },
    isPublicHoliday() {
      return (date) => {
        // 周末一般算假日，除非调休导致变成工作日
        const publicHoliday = ['六', '日']
        return publicHoliday.includes(getWeekday(date))
      }
    },
    isUser() {
      return (date) => {
        const obj = this.dutyCalendarDict[date]
        if (obj) {
          return obj.calendar_plan.find(item => item.personnel === this.userUUID)
        } else return false
      }
    }
  },
  watch: {
    value: {
      immediate: true,
      handler(newValue, oldValue) {
        const om = oldValue ? oldValue.getMonth() : null
        const nm = newValue.getMonth()
        if (nm !== om) this.fetchData()
      }
    }
  },
  methods: {
    // 获取当前月份的值班日历数据列表
    async fetchData() {
      this.loading = true
      // 获取当前年月
      const ym = datetimeFormat(this.value, 'YYYY-MM')
      // const allRes = await Promise.all([
      //   DutyCalendar.getList({ limit: -1, ym: ym }),
      //   DutyClassify.getList({}, 'dictionary/'), // 获取值班类型列表，用于展示预估津贴、补贴
      //   DutyPersonnel.getList({}, 'dictionary/'), // 获取值班人员列表
      //   HolidaysAndFestivals.getList({ limit: -1, ym: ym }) // 获取当月所有的节日、假日
      // ])
      const allRes = await multipleRequests([
        DutyCalendar.getList({ limit: -1, ym: ym }),
        DutyClassify.getList({}, 'dictionary/'), // 获取值班类型列表，用于展示预估津贴、补贴
        DutyPersonnel.getList({}, 'dictionary/'), // 获取值班人员列表
        HolidaysAndFestivals.getList({ limit: -1, ym: ym }) // 获取当月所有的节日、假日
      ])
      // 把值班日历列表转为以date为键值的字典
      if (allRes[0].data) this.dutyCalendarDict = ArrayToDictionary(allRes[0].data.results, 'date', false)
      // 把值班类型列表转为以key为键值的字典
      if (allRes[1].data) {
        this.dutyClassifyDict = ArrayToDictionary(allRes[1].data, 'id')
        try {
          this.dutyClassifyDivide = allRes[1].data[1].sequence
        } catch (e) {
          this.dutyClassifyDivide = 2
        }
      }
      // 把值班人员列表转为以id为键值的字典
      if (allRes[2].data) this.dutyPersonnelDict = ArrayToDictionary(allRes[2].data, 'id')
      // 把当月假日数据列表转为以id为键值的字典
      if (allRes[3].data) this.holidaysAndFestivalsDict = ArrayToDictionary(allRes[3].data.results, 'date')
      this.loading = false
    },
    // 操作数据表任一对象【单个】
    actionObject(data) {
      // 当前月份的日期允许点击编辑，其它只允许点击跳转到相邻月份
      if (data.type === 'current-month') {
        // 根据当前点击的日期，从之前获取的值班计划数据匹配，若匹配到，则表示现在要编辑，否则视为新增
        const action = this.dutyCalendarDict[data.day]
        this.currDate = data.day
        if (action === undefined) {
          this.formData = undefined
          this.dialogTitle = '新增【值班计划】'
        } else {
          this.formData = action
          this.dialogTitle = '编辑【值班计划】'
        }
        this.dialogVisible = true
      }
    }
  }
}
</script>

<style scoped>
  ::v-deep .el-dialog {
    width: 750px;
  }

  .el-calendar {
    min-width: 1080px;
  }

  .calendar-custom-grid {
    display: flex;
    height: 100%;
    /*padding: 20px 10px;*/
    padding: 5px;
  }

  .grid-item {
    flex: 1;
    margin: auto;
  }

  .date-number {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    font-style: italic;
    font-family: auto;
    margin-bottom: 10px;
  }

  .department-person-item {
    margin: 7px 0;
    padding-left: 10px;
  }

  .department-label {
    font-size: 12px;
    border: 1px solid #dddddd;
    /*padding: 3px;*/
    padding: 2px;
    border-radius: 100%;
    /*margin-right: 5px;*/
    margin-right: 2px;
    color: #fff;
    background: green;
  }

  .person-name {
    font-size: 12px;
    /*font-size: 14px;*/
    /*vertical-align: middle;*/
  }

   .key-personnel {
     /*font-size: 16px;*/
   }

  ::v-deep .el-calendar-table .el-calendar-day {
    height: 110px;
    position: relative;
    overflow: hidden;
    padding: 0;
  }

  .day-off-icon {
    position: absolute;
    top: -5px;
    left: -20px;
    padding: 8px 20px 3px 20px;
    color: #ffffff;
    transform: rotate(-45deg)
  }

  .holidays-festivals-name {
    position: absolute;
    left: 20px;
    top: 0;
    padding: 2px 0 2px 10px;
    font-size: 12px;
    color: #ffffff;
    z-index: 1;
    width: 94px;
    white-space: nowrap;
  }

  .beautify-angle-icon {
    position: absolute;
    border: 12px solid;
    transform: rotate(-45deg);
    left: 82px;
    top: -12px;
    z-index: -1;
  }

  ::v-deep .el-calendar-table td.is-today {
    border: 2px solid;
    background: #deeeff;
  }

  /*::v-deep .el-calendar-table:not(.is-range) td.next {!*隐藏下个月的日期*!*/
  /*  visibility:hidden;*/
  /*}*/

  /*::v-deep .el-calendar-table:not(.is-range) td.prev {!*隐藏上个月的日期*!*/
  /*  visibility: hidden;*/
  /*}*/
</style>
