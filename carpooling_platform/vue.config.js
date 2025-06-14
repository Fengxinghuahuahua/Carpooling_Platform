const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    client: {
      overlay: false
    },
    proxy: {
      '/api':{
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
