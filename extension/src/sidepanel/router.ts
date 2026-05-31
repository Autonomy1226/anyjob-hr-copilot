import { createRouter, createWebHashHistory } from 'vue-router'
import ResumePage from './pages/ResumePage.vue'
import MatchingPage from './pages/MatchingPage.vue'
import MessagePage from './pages/MessagePage.vue'
import DashboardPage from './pages/DashboardPage.vue'

export const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', redirect: '/resume' },
    { path: '/resume', name: 'resume', component: ResumePage },
    { path: '/matching', name: 'matching', component: MatchingPage },
    { path: '/message', name: 'message', component: MessagePage },
    { path: '/dashboard', name: 'dashboard', component: DashboardPage },
  ],
})
