<template>
  <div id="app-container">
    <AppHeader :title="headerTitle" v-if="showHeaderAndFooter" />
    <main class="main-content" :class="{ 'no-padding': !showHeaderAndFooter }"> <!-- 动态添加class -->
      <router-view v-slot="{ Component }">
          <component :is="Component" />

      </router-view>
    </main>
    <AppFooter v-if="showHeaderAndFooter" />
  </div>
</template>

<script>
// import UserAuth from './views/UserAuth.vue'
// import ProfilePage from './components/ProfileContent.vue'
import AppHeader from './components/AppHeader.vue'; // 引入页头组件
import AppFooter from './components/AppFooter.vue'; // 引入页脚组件
export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter
    // UserAuth,
    // ProfilePage
  },
  computed: {
    headerTitle() {
       if (this.$route.meta && this.$route.meta.title) {
        return this.$route.meta.title;
      }
      switch (this.$route.name) {
        case 'HomePage': return '拼车首页';
        case 'TripDetailPage': return '行程详情';
        case 'PublishTripPage': return '发布行程';
        case 'SearchTripPage': return '行程搜索';
        case 'LoginPage': return '用户登录';
        case 'PersonalPage': return '个人中心';
        case 'AdminPage': return '管理后台';
        default: return '拼车平台';
      }
    },
    showHeaderAndFooter() {
      // 定义哪些页面的路由名称应该显示页头和页脚
      const pagesWithHeaderFooter = [
        'HomePage',
        'ProfileContentPage',
        'SearchTripPage',
        'TripDetailPage',
        'PublishTripPage',
        'PersonalPage'
      ];
      return pagesWithHeaderFooter.includes(this.$route.name);
    },
    keepAliveComponents() {
      return ['HomePage', 'SearchTripPage'];
    }
  }
}
</script>

<style>
body {
  margin: 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  box-sizing: border-box;
  user-select: none;
}
*, *::after, *::before {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  user-select: none;
}
</style>
