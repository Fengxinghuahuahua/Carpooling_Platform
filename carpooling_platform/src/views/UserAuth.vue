<template>
  <div class="auth-container">
    <div class="mid-container">
      <el-card class="auth-card" shadow="hover" :body-style="{ padding: '20px' }">
        <div class="toggle-tabs">
          <el-radio-group v-model="activeTab" size="large">
            <el-radio-button label="login">登录</el-radio-button>
            <el-radio-button label="register">注册</el-radio-button>
          </el-radio-group>
        </div>

        <!-- 登录表单 -->
        <el-form
          v-if="activeTab === 'login'"
          :model="loginForm"
          :rules="loginRules"
          ref="loginFormRef"
          label-width="80px"
        >
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="loginForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="loginForm.password" placeholder="请输入密码" />
          </el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
        </el-form>

        <!-- 注册表单 -->
        <el-form
          v-else
          :model="registerForm"
          :rules="registerRules"
          ref="registerFormRef"
          label-width="80px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="registerForm.phone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="registerForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="registerForm.password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input type="password" v-model="registerForm.confirmPassword" placeholder="请再次输入密码" />
          </el-form-item>
          <el-button type="primary" @click="handleRegister">注册</el-button>
        </el-form>
      </el-card>
    </div>
    <!-- 底部声明 -->
    <footer class="footer">
      © 2025 Carpooling Platform. All rights reserved.
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'UserAuth',
  setup() {
    const activeTab = ref('login')

    // 登录表单
    const loginForm = ref({
      phone: '',
      password: ''
    })
    const loginFormRef = ref(null)
    const loginRules = {
      phone: [
        { required: true, message: '手机号不能为空', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
        { pattern: /^[a-zA-Z0-9_]{6,20}$/, message: '密码格式不正确（6-20位字母、数字或下划线）', trigger: 'blur' }
      ]
    }

    // 注册表单
    const registerForm = ref({
      username: '',
      phone: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    const registerFormRef = ref(null)
    const registerRules = {
      username: [
        { required: true, message: '用户名不能为空', trigger: 'blur' },
        { min: 2, max: 20, message: '用户名长度应在2-20个字符之间', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '手机号不能为空', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '邮箱不能为空', trigger: 'blur' },
        { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '密码不能为空', trigger: 'blur' },
        { pattern: /^[a-zA-Z0-9_]{6,20}$/, message: '密码格式不正确（6-20位字母、数字或下划线）', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '确认密码不能为空', trigger: 'blur' },
        {
          validator(rule, value, callback) {
            if (value !== registerForm.value.password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }

    const handleLogin = () => {
      loginFormRef.value.validate((valid) => {
        if (valid) {
          ElMessage.success('登录成功！')
          // TODO: 发送登录请求
        }
      })
    }

    const handleRegister = () => {
      registerFormRef.value.validate((valid) => {
        if (valid) {
          ElMessage.success('注册成功！')
          // TODO: 发送注册请求
        }
      })
    }

    return {
      activeTab,
      loginForm,
      loginFormRef,
      loginRules,
      registerForm,
      registerFormRef,
      registerRules,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column; /* 使内容和底部声明垂直排列 */
  justify-content: flex-start;
  align-items: flex-start; /* 将内容对齐到左侧 */
  height: 100vh;
  background: url('../assets/背景.png') no-repeat center center; /* 添加背景图片 */
  background-size: cover; /* 使背景图片覆盖整个页面 */
  background-attachment: fixed; /* 固定背景图片，防止滚动 */
  background-position: left; /* 确保图片居中显示 */
}

.mid-container {
  display: flex;
  margin-top: 260px; /* 留出顶部空间，避免与Logo重叠 */
  margin-left: 150px; /* 添加左侧内边距，与Logo左侧对其 */
}

.auth-card {
  margin-top: auto; /* 将 footer 推到页面底部 */
  width: 400px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background-color: rgba(228, 236, 247, 0.9); /* 设置背景颜色并调整透明度 */
  border-radius: 12px;
  position: relative; /* 确保不受全局样式影响 */
}

.footer {
  align-self: center; /* 将 footer 居中对齐 */
  margin-top: auto; /* 将 footer 推到页面底部 */
  text-align: center;
  padding: 10px 0;
  font-size: 14px;
  color: #666;
  background-color: transparent; /* 保持背景透明 */
  width: 100%;
}

.toggle-tabs {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.el-form-item {
  margin-bottom: 22px;
}

.el-form-item:last-child {
  display: flex;
  justify-content: center;
}

.el-input {
  width: 100%;
}
</style>