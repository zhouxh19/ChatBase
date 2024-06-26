import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/index.vue'

export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404.vue'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401.vue'),
    hidden: true
  },
  // {
  //   path: '/',
  //   component: Layout,
  //   redirect: '/chat',
  //   children: [
  //     {
  //       path: 'chat',
  //       name: 'Chat',
  //       component: () => import('@/views/chat/index.vue'),
  //       //using el svg icon, the elSvgIcon first when at the same time using elSvgIcon and icon
  //       meta: { title: 'Chat', elSvgIcon: 'ChatDotRound', affix: true }
  //     }
  //   ]
  // },
  {
    path: '/',
    component: Layout,
    redirect: '/knowledge/chat',
    children: [
      {
        path: '/knowledge/chat',
        name: 'KnowledgeChat',
        component: () => import('@/views/knowledge-chat/index.vue'),
        //using el svg icon, the elSvgIcon first when at the same time using elSvgIcon and icon
        meta: { title: 'KnowledgeChat', elSvgIcon: 'ChatDotSquare', affix: true }
      }
    ]
  },
  {
    path: '/database/chat',
    component: Layout,
    children: [
      {
        path: '/database/chat',
        name: 'DatabaseChat',
        component: () => import('@/views/database-chat/index.vue'),
        //using el svg icon, the elSvgIcon first when at the same time using elSvgIcon and icon
        meta: { title: 'DatabaseChat', elSvgIcon: 'Coin', affix: true }
      }
    ]
  },
  {
    path: '/multi-source/chat',
    component: Layout,
    children: [
      {
        path: '/multi-source/chat',
        name: 'MultiSourceChat',
        component: () => import('@/views/multi-source-chat/index.vue'),
        //using el svg icon, the elSvgIcon first when at the same time using elSvgIcon and icon
        meta: { title: 'MultiSourceChat', elSvgIcon: 'Menu', affix: true }
      }
    ]
  },
  {
    path: '/knowledge',
    component: Layout,
    children: [
      {
        path: '/knowledge',
        name: 'Knowledge',
        component: () => import('@/views/knowledge/index.vue'),
        //using el svg icon, the elSvgIcon first when at the same time using elSvgIcon and icon
        meta: { title: 'Knowledge', elSvgIcon: 'Collection'}
      },
      {
        path: '/knowledge/detail',
        name: 'KnowledgeDetail',
        component: () => import('@/views/knowledge/detail.vue'),
        //using el svg icon, the elSvgIcon first when at the same time using elSvgIcon and icon
        meta: { title: 'Knowledge', elSvgIcon: 'Collection', activeMenu: '/knowledge'}
      }
    ]
  },
  {
    path: '/course_chat',
    component: () => import('@/views/knowledge-chat/course_chat.vue'),
    meta: { ignoreLogin: true},
    hidden: true
  },
  { path: "/:pathMatch(.*)", redirect: "/404", hidden: true }
]

//角色和code数组动态路由
export const roleCodeRoutes = [

]
/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  // 404 page must be placed at the end !!!
  { path: "/:pathMatch(.*)", redirect: "/404", hidden: true },
]


const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0 }),
  routes: constantRoutes
})

export default router
