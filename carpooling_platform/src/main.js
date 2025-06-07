import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import './assets/global.css';
import router from "@/router/index";
import "@/mockjs/index";
// --- BEGIN: 模拟登录状态 (仅限开发环境) ---
if (process.env.NODE_ENV === 'development') {
  // 只有当 localStorage 中没有 userToken 时才进行模拟登录
  // 这样如果你通过登录界面真实登录了，就不会被覆盖
  if (!localStorage.getItem('userToken')) {
    const mockToken = 'mock-developer-token-12345';
    const mockUser = {
      id: 'devUser001',
      name: '开发模拟用户',
      email: 'dev@example.com',
      avatar: 'https://i.pravatar.cc/50?u=devUser001' // 一个随机头像服务
    };

    localStorage.setItem('userToken', mockToken);
    localStorage.setItem('currentUser', JSON.stringify(mockUser));

    console.warn("模拟登录成功！Token 和用户信息已设置到 localStorage。");
    console.log("Mock Token:", mockToken);
    console.log("Mock User:", mockUser);
  } else {
    console.log("检测到已存在的 userToken，不执行模拟登录。");
  }
}
const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')

