import { createRouter, createWebHistory } from 'vue-router'

import LoginPage from '@/views/LoginPage.vue'
import PersonalPage from '@/views/PersonalPage.vue'

import ProfileContent from '@/components/ProfileContent.vue'
import UserAuth from '@/components/UserAuth.vue'

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
              { path: '', component: ProfileContent,  meta: { requiresAuth: true }}
          ]
      }
    ]
  })

// 全局前置守卫
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token'); // 检查是否存在 token
    if (to.matched.some(record => record.meta.requiresAuth) && !token) {
        // 如果路由需要登录且没有 token，则跳转到登录页面
        next({ path: '/login' });
    } else {
        // 如果已登录或不需要登录，允许访问
        next();
    }
});

export default router
