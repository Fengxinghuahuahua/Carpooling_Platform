<template>
  <header class="app-header">
    <div class="header-content">
      <img src="@/assets/logo.png" alt="Logo" class="logo" @click="goHome" />
      <h1 class="app-title" @click="goHome">{{ title }}</h1>
      <div class="user-actions">
        <span v-if="userName" class="user-name" @click="goToPersonal">{{ userName }}</span>
        <button v-if="isLoggedIn" @click="logout" class="btn-logout">退出</button>
        <button v-else @click="goToLogin" class="btn-login">登录</button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  props: {
    title: {
      type: String,
      default: '拼车平台'
    }
  },
  data() {
    return {
      isLoggedIn: false,
      userName: ''
    };
  },
  created() {
    this.checkLoginStatus();
    window.addEventListener('login-status-changed', this.checkLoginStatus);
  },
  beforeUnmount() {
    window.removeEventListener('login-status-changed', this.checkLoginStatus);
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem('userToken');
      const user = JSON.parse(localStorage.getItem('currentUser'));
      this.isLoggedIn = !!token;
      this.userName = user ? user.name : '';
    },
    logout() {
      localStorage.removeItem('userToken');
      localStorage.removeItem('currentUser');
      this.isLoggedIn = false;
      this.userName = '';
      this.$router.push('/login');
      // 触发事件通知其他组件登录状态变化
      window.dispatchEvent(new CustomEvent('login-status-changed'));
    },
    goHome() {
      this.$router.push('/home');
    },
    goToLogin() {
      this.$router.push('/login');
    },
    goToPersonal() {
      this.$router.push('/personal');
    }
  }
};
</script>

<style scoped>
.app-header {
  background-color: #007bff; /* 主题蓝色 */
  color: white;
  padding: 0 20px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  height: 60px;
}
.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}
.logo {
  height: 40px;
  margin-right: 10px;
  cursor: pointer;
}
.app-title {
  font-size: 1.5em;
  margin: 0;
  cursor: pointer;
  font-weight: bold;
}
.user-actions {
  display: flex;
  align-items: center;
}
.user-name {
  margin-right: 15px;
  cursor: pointer;
  font-weight: 500;
}
.user-name:hover {
  text-decoration: underline;
}
.btn-logout, .btn-login {
  background-color: transparent;
  color: white;
  border: 1px solid white;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}
.btn-logout:hover, .btn-login:hover {
  background-color: rgba(255,255,255,0.2);
}
</style>