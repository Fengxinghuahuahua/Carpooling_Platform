<template>
  <footer class="app-footer">
    <router-link to="/home" class="footer-item" active-class="active">
      <span class="icon">🏠</span>
      <span>拼车</span>
    </router-link>
    <router-link to="/publish" class="footer-item" active-class="active">
      <span class="icon">➕</span>
      <span>发布</span>
    </router-link>
    <router-link to="/search" class="footer-item" active-class="active">
      <span class="icon">🔍</span>
      <span>搜索</span>
    </router-link>
    <router-link to="/personal" class="footer-item" active-class="active">
      <span class="icon">👤</span>
      <span>我的</span>
    </router-link>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
};
</script>

<style scoped>
.app-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #fff;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 5px 0;
  height: 60px;
  box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
  z-index: 1000;
}
.footer-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #888;
  font-size: 0.8em;
  padding: 5px 10px;
}
.footer-item .icon {
  font-size: 1.5em; /* 调整图标大小 */
  margin-bottom: 2px;
}
.footer-item.active {
  color: #007bff; /* 主题蓝色 */
}
</style>