<template>
  <div>
    <RouterView />
  </div>
</template>

<script>
// import UserAuth from './views/UserAuth.vue'
// import ProfilePage from './components/ProfileContent.vue'

export default {
  name: 'App',
  components: {
    // UserAuth,
    // ProfilePage
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
