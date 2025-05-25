import { createRouter, createWebHistory } from 'vue-router'

import LoginPage from '@/views/LoginPage.vue'
import PersonalPage from '@/views/PersonalPage.vue'
import AdminPage from '@/views/AdminPage.vue' 

import ProfileContent from '@/components/ProfileContent.vue'
import UserAuth from '@/components/UserAuth.vue'
import AdminUser from '@/components/AdminUser.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      component: LoginPage,
      children: [
        { path: '', component: UserAuth }
      ]
    },
    {
      path: '/personal',
      component: PersonalPage,
      meta: { requiresAuth: true }, // 需要登录才能访问
      children: [
        { path: '', component: ProfileContent, meta: { requiresAuth: true } }
      ]
    },
    {
      path: '/admin',                      // 添加后台路径
      component: AdminPage,
      meta: { requiresAuth: true, requiresAdmin: true }, // 需要登录且是管理员
      children: [
        { path: '', component: AdminUser, meta: { requiresAuth: true, requiresAdmin: true } }
      ]
    }
  ]
})


export default router;
