// src/router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { setupGuard } from './guard'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    component: () => import('@/layouts/BlankLayout.vue'),
    children: [
      {
        path: '',
        name: 'Login',
        component: () => import('@/views/login/LoginView.vue'),
      },
    ],
  },
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/DashboardView.vue'),
      },
      {
        path: 'tickets',
        name: 'TicketList',
        component: () => import('@/views/ticket/TicketListView.vue'),
      },
      {
        path: 'tickets/create',
        name: 'TicketCreate',
        component: () => import('@/views/ticket/TicketCreateView.vue'),
      },
      {
        path: 'tickets/:id',
        name: 'TicketDetail',
        component: () => import('@/views/ticket/TicketDetailView.vue'),
      },
      {
        path: 'knowledge',
        name: 'KnowledgeList',
        component: () => import('@/views/knowledge/KnowledgeListView.vue'),
      },
      {
        path: 'knowledge/:id',
        name: 'KnowledgeDetail',
        component: () => import('@/views/knowledge/knowledgeDetailView.vue'),
      },
      {
        path: 'ai/chat',
        name: 'Chat',
        component: () => import('@/views/ai/ChatView.vue'),
      },
    ],
  },
  // 404 兜底
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

setupGuard(router)

export default router