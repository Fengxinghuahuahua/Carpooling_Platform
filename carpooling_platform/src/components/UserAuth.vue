<template>
  <div class="body">
    <div class="main-box">
      <!-- 注册表单 -->
      <div :class="['container', 'container-register', { 'is-txl': isLogin }]">
        <form>
          <h2 class="title">注册</h2>
          <div class="form__icons">
            <img class="form__icon" src="@/assets/images/wechat.png" alt="微信登录" />
            <img class="form__icon" src="@/assets/images/alipay.png" alt="支付宝登录" />
            <img class="form__icon" src="@/assets/images/QQ.png" alt="QQ登录" />
          </div>
          <span class="text">或使用邮箱进行注册</span>
          <div v-if="registerError" class="error-message">{{ registerError }}</div>
          <input class="form__input" type="text" placeholder="请输入用户名" v-model="registerForm.name" />
          <input class="form__input" type="text" placeholder="请输入邮箱" v-model="registerForm.email" />
          <input class="form__input" type="text" placeholder="请输入手机号" v-model="registerForm.phone" />
          <input class="form__input" type="password" placeholder="请输入密码" v-model="registerForm.password" />
          <input class="form__input" type="password" placeholder="请确认密码" v-model="registerForm.confirmPassword" />
          <div class="form__button" @click="register">立即注册</div>
        </form>
      </div>

      <!-- 登录表单 -->
      <div :class="['container', 'container-login', { 'is-txl is-z200': isLogin }]">
        <form>
          <h2 class="title">登录</h2>
          <div class="form__icons">
            <img class="form__icon" src="@/assets/images/wechat.png" alt="微信登录" />
            <img class="form__icon" src="@/assets/images/alipay.png" alt="支付宝登录" />
            <img class="form__icon" src="@/assets/images/QQ.png" alt="QQ登录" />
          </div>
          <span class="text">或使用用户名登录</span>
          <div v-if="loginError" class="error-message">{{ loginError }}</div>
          <input class="form__input" type="text" placeholder="用户名/手机号/邮箱" v-model="loginForm.identifier" />
          <input class="form__input" type="password" placeholder="请输入密码" v-model="loginForm.password" />
          <div class="form__button" @click="login">立即登录</div>
        </form>
      </div>

      <!-- 切换按钮 -->
      <div :class="['switch', { 'login': isLogin }]">
        <div class="switch__circle"></div>
        <div class="switch__circle switch__circle_top"></div>
        <div class="switch__container">
          <h2>{{ isLogin ? '您好 !' : '欢迎回来 !' }}</h2>
          <p>
            {{
              isLogin
                ? '如果您还没有账号，请点击下方立即注册按钮进行账号注册'
                : '如果您已经注册过账号，请点击下方立即登录按钮进行登录'
            }}
          </p>
          <div class="form__button" @click="toggleLogin">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router'; // 引入 Vue Router

export default {
  name: 'UserAuth',
  setup() {
    // 状态
    const isLogin = ref(true);

    const router = useRouter(); // 使用 Vue Router

    // 登录表单
    const loginForm = ref({
      identifier: '', // 用户名/手机号/邮箱
      password: '',
    });

    const loginError = ref('');

    // 注册表单
    const registerForm = ref({
      name: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
    });

    const registerError = ref('');

    // 切换登录/注册
    const toggleLogin = () => {
      isLogin.value = !isLogin.value;
      loginError.value = '';
      registerError.value = '';
    };

    // 登录方法
    const login = async () => {
      const { identifier, password } = loginForm.value;

      // 校验登录表单
      if (!identifier) {
        loginError.value = '请输入用户名/手机号/邮箱';
        return;
      }
      if (!password) {
        loginError.value = '请输入密码';
        return;
      }

      try {
        const response = await axios.post('/api/auth/login', { identifier, password });
        if (response.status !== 200) {
          console.error('登录失败:', response);
          loginError.value = '登录失败';
          throw new Error('登录失败');
        }
        console.log('登录成功:', response.data);
        loginError.value = ''; // 清空错误信息

        // TODO：此处只是模拟登录成功，后续连接到后端后此处需要进行修改
        localStorage.setItem('token', response.data.token); // 假设后端返回了一个 token
        
        router.push('/personal'); // 登录成功后跳转到个人主页
      } catch (error) {
        loginError.value = error.response?.data?.error || '登录失败，请稍后重试';
      }
    };

    // 注册方法
    const register = async () => {
      const { name, email, phone, password, confirmPassword } = registerForm.value;

      // 校验用户名
      if (!name || name.length < 2 || name.length > 20 || /\s/.test(name)) {
        registerError.value = '用户名必须为2-20个字符，且不能包含空格';
        return;
      }

      // 校验邮箱
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        registerError.value = '请输入有效的邮箱地址';
        return;
      }

      // 校验手机号
      if (!phone || !/^1[3-9]\d{9}$/.test(phone)) {
        registerError.value = '请输入有效的手机号';
        return;
      }

      // 校验密码
      if (!password || !/^[a-zA-Z0-9_]{6,20}$/.test(password)) {
        registerError.value = '密码必须为6-20个字符，由字母、数字或下划线组成';
        return;
      }

      // 校验确认密码
      if (password !== confirmPassword) {
        registerError.value = '两次输入的密码不一致';
        return;
      }

      try {
        const response = await axios.post('/api/auth/register', { name, email, phone, password });
        ElMessage.success('注册成功！');
        console.log('注册成功:', response.data);
        registerError.value = ''; // 清空错误信息
        toggleLogin(); // 注册成功后切换到登录页面
      } catch (error) {
        registerError.value = error.response?.data?.error || '注册失败，请稍后重试';
      }
    };

    return {
      isLogin,
      loginForm,
      loginError,
      registerForm,
      registerError,
      toggleLogin,
      login,
      register,
    };
  },
};
</script>

<style lang="scss" scoped>
.body {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Montserrat", sans-serif;
  font-size: 12px;
  background-image: url("@/assets/images/background.jpg");
  color: #a0a5a8;
}

.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 10px;
}

.main-box {
  position: relative;
  width: 1000px;
  min-width: 1000px;
  min-height: 600px;
  height: 600px;
  padding: 25px;
  background-color: #ecf0f3;
  box-shadow: 1px 1px 100px 10px #ecf0f3;
  border-radius: 12px;
  overflow: hidden;

  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    width: 600px;
    height: 100%;
    padding: 25px;
    background-color: #ecf0f3;
    transition: all 1.25s;

    form {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      width: 100%;
      height: 100%;
      color: #a0a5a8;

      .form__icon {
        object-fit: contain;
        width: 30px;
        margin: 0 5px;
        opacity: 0.5;
        transition: 0.15s;

        &:hover {
          opacity: 1;
          transition: 0.15s;
          cursor: pointer;
        }
      }

      .title {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }

      .text {
        margin-top: 30px;
        margin-bottom: 12px;
      }

      .form__input {
        width: 350px;
        height: 40px;
        margin: 4px 0;
        padding-left: 25px;
        font-size: 13px;
        letter-spacing: 0.15px;
        border: none;
        outline: none;
        background-color: #ecf0f3;
        transition: 0.25s ease;
        border-radius: 8px;
        box-shadow: inset 2px 2px 4px #d1d9e6, inset -2px -2px 4px #f9f9f9;

        &::placeholder {
          color: #a0a5a8;
        }
      }
    }
  }

  .container-register {
    z-index: 100;
    left: calc(100% - 600px);
  }

  .container-login {
    left: calc(100% - 600px);
    z-index: 0;
  }

  .is-txl {
    left: 0;
    transition: 1.25s;
    transform-origin: right;
  }

  .is-z200 {
    z-index: 200;
    transition: 1.25s;
  }

  .switch {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 400px;
    padding: 50px;
    z-index: 200;
    transition: 1.25s;
    background-color: #ecf0f3;
    overflow: hidden;
    box-shadow: 4px 4px 10px #d1d9e6, -4px -4px 10px #f9f9f9;
    color: #a0a5a8;

    .switch__circle {
      position: absolute;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      background-color: #ecf0f3;
      box-shadow: inset 8px 8px 12px #d1d9e6, inset -8px -8px 12px #f9f9f9;
      bottom: -60%;
      left: -60%;
      transition: 1.25s;
    }

    .switch__circle_top {
      top: -30%;
      left: 60%;
      width: 300px;
      height: 300px;
    }

    .switch__container {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      position: absolute;
      width: 400px;
      padding: 50px 55px;
      transition: 1.25s;

      h2 {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }

      p {
        font-size: 14px;
        letter-spacing: 0.25px;
        text-align: center;
        line-height: 1.6;
      }
    }
  }

  .login {
    left: calc(100% - 400px);

    .switch__circle {
      left: 0;
    }
  }

  .form__button {
    width: 180px;
    height: 50px;
    border-radius: 25px;
    margin-top: 50px;
    text-align: center;
    line-height: 50px;
    font-size: 14px;
    letter-spacing: 2px;
    background-color: #4b70e2;
    color: #f9f9f9;
    cursor: pointer;
    box-shadow: 8px 8px 16px #d1d9e6, -8px -8px 16px #f9f9f9;

    &:hover {
      box-shadow: 2px 2px 3px 0 rgba(255, 255, 255, 50%),
        -2px -2px 3px 0 rgba(116, 125, 136, 50%),
        inset -2px -2px 3px 0 rgba(255, 255, 255, 20%),
        inset 2px 2px 3px 0 rgba(0, 0, 0, 30%);
    }
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-box {
    width: 100%;
    min-width: unset;
    height: auto;
    padding: 15px;
  }

  .container {
    width: 100%;
    position: relative;
    padding: 10px;

    form {
      .form__input {
        width: 100%;
      }
    }
  }

  .switch {
    width: 100%;
    height: auto;
    position: relative;
    padding: 20px;

    .switch__container {
      width: 100%;
      padding: 20px;
    }
  }
}
</style>