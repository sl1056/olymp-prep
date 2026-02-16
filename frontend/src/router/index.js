import { createRouter, createWebHistory } from 'vue-router'
//import AutorisationView from './views/AutorisationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: () => import('../views/MainView.vue'),
    },
    {
      path: '/auth',
      name: 'auth',
      component: () => import('../views/AuthView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
    },
    {
      path: '/training/result',
      name: 'trainResult',
      component: () => import('../views/training/trainResult.vue'),
    },
    {
      path: '/training/start',
      name: 'startTraning',
      component: () => import('../views/training/startView.vue'),
    },
    {
      path: '/training/study',
      name: 'trainStudy',
      component: () => import('../views/training/trainStudyView.vue'),
    },
    {
      path: '/profile/stats',
      name: 'stats',
      component: () => import('../views/ProfileStatsView.vue'),
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('../views/StudyViewNotAnswer.vue'),
      meta: {
        requiresAuth: false // Разрешаем доступ всем
      }
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/StudyView.vue'),
    },
    {
      path: '/PvP',
      name: 'pvp',
      component: () => import('../PvP/main.vue'),
    },
    {
      path: '/PvP/create',
      name: 'create',
      component: () => import('../PvP/createMatch.vue'),
    },
    {
      path: '/PvP/create/wait',
      name: 'wait',
      component: () => import('../PvP/pvpWait.vue'),
    },
     {
      path: '/PvP/Answer',
      name: 'answer',
      component: () => import('../PvP/pvpAnswer.vue'),
    },
    {
      path: '/profile/achievements',
      name: 'achievements',
      component: () => import('../views/AchievView.vue'),
    },
    {
      path: '/PvP/Result',
      name: 'result',
      component: () => import('../PvP/pvpResult.vue'),
    },
    {
      path: '/register',
      name: 'register',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/RegisterView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('authToken');
    
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/auth');
    } else {
        next();
    }
});

export default router
