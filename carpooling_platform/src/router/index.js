import { createRouter, createWebHistory } from 'vue-router'

import LoginPage from '@/views/LoginPage.vue'
import PersonalPage from '@/views/PersonalPage.vue'
import AdminPage from '@/views/AdminPage.vue' 
import HomePage from '@/views/HomePage.vue';
import TripDetailPage from '@/views/TripDetailPage.vue';
import PublishTripPage from '@/views/PublishTripPage.vue';
import SearchTripPage from '@/views/SearchTripPage.vue';
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
      name: 'PersonalPage',
      component: PersonalPage,
      meta: { requiresAuth: true }, // 需要登录才能访问
      children: [
        { path: '',  name: 'ProfileContentPage',component: ProfileContent, meta: { requiresAuth: true } }
      ]
    },
    {
        path: '/home',
        name: 'HomePage',
        component: HomePage,
        meta: { requiresAuth: true }
    },
    {
        path: '/trip/:id', // 动态路由参数 :id
        name: 'TripDetailPage',
        component: TripDetailPage,
        meta: { requiresAuth: true },
        props: true // 将路由参数作为 props 传递给组件
    },
    {
        path: '/publish',
        name: 'PublishTripPage',
        component: PublishTripPage,
        meta: { requiresAuth: true }
    },
    {
        path: '/search',
        name: 'SearchTripPage',
        component: SearchTripPage,
        meta: { requiresAuth: true }
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
