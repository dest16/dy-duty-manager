<template>
  <div class="vue-calendar-ui" :class="{ 'vue-calendar-small': min }">
    <div class="cv-controlBox">
      <div class="cv-title" :style="{ color: titleColor }">
        {{ today | formatDate }}
        <i
          class="ivcufont ivcu-liulangengduo cv-arrowRight"
          :style="{ color: arrowColor }"
          @click="handlePrevAndNexMonth('next')"
        />
        <i
          class="ivcufont ivcu-liulangengduo cv-arrowLeft"
          :style="{ color: arrowColor }"
          @click="handlePrevAndNexMonth('prev')"
        />
      </div>
    </div>
    <div class="cv-contentBox">
      <ul class="cv-top" :style="{ color: weeklabelColor }">
        <li v-for="(item, index) in labelArr" :key="index" class="cv-label">
          周{{ item }}
        </li>
      </ul>
      <ul class="cv-main">
        <li
          v-for="(item, index) in arrList"
          :key="index"
          class="cv-item"
          :class="{
            'cv-prev': item.whitchMonth === 'prev',
            'cv-next': item.whitchMonth === 'next',
          }"
        >
          <div
            class="cv-date"
            :class="{
              'cv-today': item.isToday,
            }"
            :style="{
              'background-color': item.isBirthday
                ? birthdaybgColor
                : item.isToday
                ? crrentdaybgColor
                : item.date === clickDay
                ? clickdaybgColor
                : index === mouseIndex
                ? hoverbgColor
                : itembgColor,
              color: item.isBirthday
                ? birthdaylabelColor
                : item.isToday
                ? crrentdaylabelColor
                : item.date === clickDay
                ? clickdaylabelColor
                : index === mouseIndex
                ? hoverlabelColor
                : item.whitchMonth === 'prev'
                ? prevColor
                : item.whitchMonth === 'next'
                ? nextColor
                : itemlabelColor,
            }"
            @mouseenter="mouseIndex = index"
            @mouseleave="mouseIndex = null"
            @click="handleClickDate(item)"
          >
            <!--
            上面style匹配
            0、生日样式放最大
            1、当天的样式权重第2
            2、点击的效果放第3
            3、hover的效果放第4
            4、最后是默认的样式
           -->
            {{ item.id }}
            <span
              v-if="item.mark && item.userPopover"
              class="cv-click-Box"
              @click="showPopover(item)"
            />
            <img
              v-if="item.isBirthday"
              class="cv-today-birthday"
              :src="birthdayImg"
              alt=""
            />
          </div>
          <span
            v-if="item.mark"
            class="cv-circle"
            :class="{ 'cv-circle-label': item.isLabel }"
            :style="{ 'background-color': item.color, color: item.color }"
          >
            <span v-html="item.isLabel ? item.label : ''" />
            <span
              v-if="item.mark && item.userPopover"
              class="cv-click-Box"
              @click="showPopover(item)"
            />
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
// 日历插件
// import cv from 'vue-calendar-ui'
// Vue.use(cv)
import util from './util'

export default {
  name: 'SxcCalendar',
  filters: {
    formatDate(date) {
      return `${date.getFullYear()}年 ${date.getMonth() + 1}月`
    }
  },
  props: {
    //  sundayStart: false,//  默认是周一开始，周一或周天开始相应的位置也要改一下
    min: {
      type: Boolean,
      default: false
    },
    sundayStart: {
      type: Boolean,
      default: false
    },
    titlebgColor: {
      //  title颜色，默认f5f7fa
      type: String,
      default: '#f5f7fa'
    },
    titleColor: {
      //  title字体颜色，默认333333
      type: String,
      default: '#333333'
    },
    weeklabelColor: {
      // 礼拜几字体颜色，默认9da5b1
      type: String,
      default: '#9da5b1'
    },
    arrowColor: {
      // 箭头颜色，默认4b7df6
      type: String,
      default: '#4b7df6'
    },
    itembgColor: {
      // 默认日期背景颜色，默认fff
      type: String,
      default: '#fff'
    },
    itemlabelColor: {
      // 默认日期字体颜色，默认333333
      type: String,
      default: '#333333'
    },
    birthdayImg: {
      // 生日顶部图片
      type: String,
      default: util.birthdayImg
    },
    birthdaybgColor: {
      // 当天生日背景颜色，默认#FFF5E7
      type: String,
      default: '#FFF5E7'
    },
    birthdaylabelColor: {
      // 当天生日字体颜色，默认fff
      type: String,
      default: '#333333'
    },
    crrentdaybgColor: {
      // 今天的背景颜色，默认4b7df6
      type: String,
      default: '#4b7df6'
    },
    crrentdaylabelColor: {
      // 今天的字体颜色，默认fff
      type: String,
      default: '#fff'
    },
    clickdaybgColor: {
      // 当前点击日期的背景颜色，默认rgba(51, 51, 51,0.8)
      type: String,
      default: 'rgba(51, 51, 51,0.8)'
    },
    clickdaylabelColor: {
      // 当前点击日期的字体颜色，默认fff
      type: String,
      default: '#fff'
    },
    hoverbgColor: {
      // 鼠标经过背景颜色，默认4b7df6
      type: String,
      default: '#4b7df6'
    },
    hoverlabelColor: {
      // 鼠标经过字体颜色，默认#fff
      type: String,
      default: '#fff'
    },
    prevColor: {
      // 当月之前的日期颜色，默认cccccc
      type: String,
      default: '#cccccc'
    },
    nextColor: {
      // 当月之后的日期颜色，默认cccccc
      type: String,
      default: '#cccccc'
    },
    markArr: {
      // 需要标记的日期列表
      type: Array,
      default: () => {
        return [
          //  {
          //    date: '2021/05/24', // YYYY-MM-DD
          //    color: '#EE1E1E', // 图标或字的颜色
          //    isLabel: false,
          //    label: '旷旷旷旷旷旷旷旷',
          //    userPopover: true, // 默认false
          //    markContent: '<span style='color:red'>今天是个好日子</span>', // 需要标注的内容
          //    renderHtml: true, // 需要标注的内容是否采用渲染html的格式
          //  },
          //  {
          //    date: '2021/05/23', // YYYY-MM-DD
          //    color: '#EE1E1E', // 图标或字的颜色
          //    isLabel: true,
          //    label: '旷旷旷旷旷旷旷旷',
          //    userPopover: true, // 默认false
          //    markContent: '<span style='color:red'>今天是个好日子</span>', // 需要标注的内容
          //    renderHtml: true, // 需要标注的内容是否采用渲染html的格式
          //  },
        ]
      }
    },
    birthdayArr: {
      // 需要标记的日期列表
      type: Array,
      default: () => {
        return [
          // '2021/05/31','2021/05/30"
        ]
      }
    }
  },
  data() {
    return {
      title: '',
      today: new Date(),
      clickDay: null,
      labelArrBackup: ['一', '二', '三', '四', '五', '六'],
      labelArr: ['一', '二', '三', '四', '五', '六'], // '日'由是否星期天为起始日决定
      arrList: [],
      mouseIndex: null // 当前鼠标经过的时间
    }
  },
  watch: {
    markArr: {
      handler() {
        this.initMarkContent()
      },
      deep: true
    },
    birthdayArr: {
      handler() {
        this.initBirthday()
      },
      deep: true
    }
  },
  created() {
    const sundayStart = this.sundayStart
    util.sundayStart = sundayStart
    if (sundayStart) {
      this.labelArr = ['日', ...this.labelArrBackup]
    } else {
      this.labelArr = [...this.labelArrBackup, '日']
    }
    this.today = util.strToDateObj(this.today) // 先初始化时间，保证为date对象
    this.getList()
  },
  methods: {
    getList() {
      this.arrList = util.getMonthList(this.today)
      this.initMarkContent()
      this.initBirthday()
    },
    initMarkContent() {
      // 初始化需要mark的信息
      this.arrList.filter(day => !['prev', 'next'].includes(day.whitchMonth)).forEach((item, index) => {
        item.mark = false
        const markItem = this.markArr[index]
        // const markItem = this.markArr.find(
        //   (list) =>
        //     util.dateFormatStr(new Date(list.date)) ===
        //     util.dateFormatStr(new Date(item.date))
        // )
        if (markItem) Object.assign(item, markItem, { mark: true })
      })
      this.$forceUpdate()
    },
    initBirthday() {
      // 初始化需要生日信息
      this.arrList.forEach((item) => {
        const io = this.birthdayArr.some((date) => {
          return util.dateFormatStr(new Date(date)) === item.date
        })
        Object.assign(item, { isBirthday: io })
      })
      this.$forceUpdate()
    },
    handlePrevAndNexMonth(type) {
      // 点击获取下或下个月数据
      const today = this.today
      this.today = util.resetprevOrNextDateObj(today, type)
      this.$emit('onchangemonth', {
        day1: this.today,
        type
      })
      this.getList()
    },
    jumpToMonth(date) {
      // 点击获取指定月数据
      this.today = util.strToDateObj(date) // 先初始化时间，保证为date对象
      this.getList()
    },
    jumpToDay(date) {
      // 跳转到指定日期
      this.today = util.strToDateObj(date) // 先初始化时间，保证为date对象
      this.clickDay = util.dateFormatStr(this.today)
      this.getList()
    },
    showPopover(item) {
      // 点击展示popover
      this.$SHOW_CV_POPOVER(item)
    },
    handleClickDate(item) {
      // 点击日期
      const date = item.date
      this.clickDay = date
      item.whitchMonth !== 'current' && this.jumpToMonth(date)
      this.$emit('onclickdate', item)
    }
  }
}
</script>

<style scoped>
  html,
  body,
  .vue-calendar-ui,
  .vue-calendar-ui * {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .vue-calendar-ui {
    width: 100%;
    /* height: 100%; */
    overflow: hidden;
    min-width: 460px;
    border: 1px solid #E2E3E7;
    border-radius: 12px;
    /* min-height: 394px; */
  }
  .cv-controlBox {
    width: 100%;
    height: 40px;
    padding: 0 22px;
    padding-top: 20px;
    box-sizing: border-box;
    position: relative;
    text-align: left;
  }
  .cv-title {
    font-size: 20px;
    color: #333333;
    font-weight: 500;
    line-height: 1;
  }
  .cv-arrowLeft {
    float: right;
    width: 20px;
    height: 20px;
    font-size: 20px;
    margin-right: 20px;
    transform: rotate(-180deg);
    transform-origin: center;
    cursor: pointer;
    color: #3B3E66;
  }
  .cv-arrowRight {
    float: right;
    width: 20px;
    height: 20px;
    font-size: 20px;
    cursor: pointer;
    color: #3B3E66;
  }
  .cv-contentBox {
    float: left;
    width: 100%;
    padding-bottom: 30px;
    box-sizing: border-box;
  }
  .cv-top {
    float: left;
    width: 100%;
    margin: 30px 0;
    font-size: 16px;
    color: #9da5b1;
    padding: 0 2%;
    box-sizing: border-box;
  }
  .cv-top .cv-label {
    float: left;
    width: 14.28571428%;
    text-align: center;
    line-height: 1;
    margin-left: -1px;
  }
  .cv-main {
    float: left;
    width: 100%;
    padding: 0 2%;
    box-sizing: border-box;
  }
  .cv-item {
    float: left;
    width: 14.28571428%;
    height: 105px;
    text-align: center;
    line-height: 1;
    padding: 8px 0;
    position: relative;
    border: 1px solid #dddddd;
    margin-top: -1px;
    margin-left: -1px;
  }
  .cv-date {
    display: block;
    margin: 0 auto;
    width: 36px;
    height: 36px;
    line-height: 36px;
    border-radius: 50%;
    font-size: 14px;
    color: #333333;
    cursor: pointer;
    position: relative;
  }
  .cv-prev .cv-date,
  .cv-next .cv-date {
    color: #cccccc;
  }
  .cv-click-Box{
      position: absolute;
      width: 100%;
      height: 100%;
      left: 0;
      top: 0;
      cursor: pointer;
  }
  .cv-today {
    background-color: #4b7df6;
    color: #fff;
  }
  .cv-date:hover{
      background-color: #4B7DF6;
      color: #fff;
  }
  .cv-circle{
      width: 6px;
      height: 6px;
      left: 50%;
      bottom: -8px;
      margin-left: -3px;
      background-color: #4B7DF6;
      border-radius: 50%;
  }
  .cv-circle-label{
      background-color: transparent !important;
      font-size: 12px;
      width: 100%;
      height: auto;
      line-height: normal;
      white-space: nowrap;
      text-overflow: ellipsis;
      text-align: center;
      overflow: hidden;
      left: 0;
      margin-left: 0;
      bottom: -15px;
  }
  .cv-today-birthday{
    position: absolute;
    right: -5px;
    top: -14px;
    width: 25px;
    height: 25px;
  }

  /* small */
  .vue-calendar-small{
    min-width: 320px;
  }
  .vue-calendar-small .cv-arrowLeft,.vue-calendar-small .cv-arrowRight{
    top: 16px;
  }
  .vue-calendar-small .cv-top {
    margin-top: 20px;
  }
  .vue-calendar-small .cv-item {
    margin-top: 20px;
  }
  .vue-calendar-small .cv-date {
    width: 26px;
    height: 26px;
    line-height: 26px;
  }
  .vue-calendar-small .cv-contentBox{
    padding-bottom: 20px;
  }
</style>
