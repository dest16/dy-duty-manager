<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
      <div class="title-container">
        <p class="title-logo">
          <img :src="logo" :alt="title">
        </p>
        <h3 class="title">{{ title }}</h3>
      </div>
      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="请输入用户名"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>
      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="请输入密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>
      <el-button
        :loading="loading"
        type="primary"
        style="width:100%;margin-bottom:30px;"
        @click.native.prevent="handleLogin"
      >
        登 录
      </el-button>
    </el-form>
    <!-- 流星效果 -->
    <div class="liuxing-box">
      <div class="liuxing liuxing1 liuxingFla" />
      <div class="liuxing liuxing2 liuxingFla2" />
      <div class="liuxing liuxing3 liuxingFla3" />
      <div class="liuxing liuxing4 liuxingFla4" />
      <div class="liuxing liuxing5 liuxingFla5" />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getCSRFToken } from '@/api/csrf'

export default {
  name: 'Login',
  data() {
    // 自定义规则验证用户名
    const validateUsername = (rule, value, callback) => {
      if (value.length < 4) {
        callback(new Error('请输入有效的用户名'))
      } else {
        callback()
      }
    }
    // 自定义规则验证密码
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('请输入长度不小于6位的密码'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  computed: {
    ...mapState('settings', {
      title: s => s.title,
      logo: s => s.logo
    })
  },
  watch: {
    $route: {
      immediate: true,
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      }
    }
  },
  created() {
    // 获取CSRF token，并保存在cookies中
    getCSRFToken()
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          const loginForm = JSON.parse(JSON.stringify(this.loginForm))
          loginForm.password = this.$rsaEncrypt(loginForm.password)
          this.$store.dispatch('user/login', loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          console.log('用户名或密码验证失败！')
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0;
      -webkit-appearance: none;
      border-radius: 0;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-image: url(/bg.jpg);
  background-repeat: no-repeat;
  background-size: 100% 100%;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
    z-index: 1;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0 auto 40px auto;
      text-align: center;
      font-weight: bold;
    }

    .title-logo {
      text-align: center;
    }

    .title-logo img {
      border-radius: 100%;
      opacity: 0.8;
      width: 80px;
      height: 80px;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}

/* 登录界面流星动画效果 */
  .liuxing-box {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    overflow: hidden;
  }

  .liuxing {
    width: 85px;
    height: 85px;
    position: absolute;
    background: url(/line.png) no-repeat;
    background-size: contain
  }

  .liuxing1 {
    top: 0;
    left: 20%
  }

  .liuxing2 {
    top: 0;
    left: 40%;
  }

  .liuxing3 {
    top: 0;
    left: 60%;
  }

  .liuxing4 {
    top: 0;
    left: 80%;
  }

  .liuxing5 {
    top: 0;
    left: 100%;
  }

  .liuxingFla {
    animation: liuxing 5s ease-in infinite
  }

  .liuxingFla2 {
    animation: liuxing2 4s ease-in infinite
  }

  .liuxingFla3 {
    animation: liuxing3 3s linear infinite
  }

  .liuxingFla4 {
    animation: liuxing4 2s linear infinite
  }

  .liuxingFla5 {
    animation: liuxing4 3s linear infinite
  }

  @keyframes liuxing {
    0% {
        transform: translate(200px,-200px)
    }

    90% {
        transform: translate(-180px,180px);
        opacity: 1
    }

    100% {
        transform: translate(-200px,200px);
        opacity: 0
    }
  }

  @keyframes liuxing2 {
    0% {
        transform: translate(200px,-200px)
    }

    90% {
        transform: translate(-480px,480px);
        opacity: 1
    }

    100% {
        transform: translate(-500px,500px);
        opacity: 0
    }
  }

  @keyframes liuxing3 {
    0% {
        transform: translate(200px,-200px)
    }

    90% {
        transform: translate(-480px,480px);
        opacity: 1
    }

    100% {
        transform: translate(-500px,500px);
        opacity: 0
    }
  }

  @keyframes liuxing4 {
    0% {
        transform: translate(200px,-200px)
    }

    90% {
        transform: translate(-180px,180px);
        opacity: 1
    }

    100% {
        transform: translate(-200px,200px);
        opacity: 0
    }
  }

  @keyframes liuxing5 {
    0% {
        transform: translate(200px,-200px)
    }

    90% {
        transform: translate(-480px,480px);
        opacity: 1
    }

    100% {
        transform: translate(-500px,500px);
        opacity: 0
    }
  }
</style>
