<template>
  <div>
    <UserAuth />
  </div>
</template>

<script>
import UserAuth from './views/UserAuth.vue'

export default {
  name: 'App',
  components: {
    UserAuth
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
}
</style>
