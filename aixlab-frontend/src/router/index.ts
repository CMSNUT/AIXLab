import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Index.vue')
      },
      {
        path: 'datasets',
        name: 'Datasets',
        component: () => import('@/views/data/DatasetList.vue')
      },
      {
        path: 'datasets/upload',
        name: 'UploadDataset',
        component: () => import('@/views/data/UploadDataset.vue')
      },
      {
        path: 'datasets/:id',
        name: 'DatasetDetail',
        component: () => import('@/views/data/DatasetDetail.vue'),
        props: true
      },
      {
        path: 'analysis',
        name: 'Analysis',
        component: () => import('@/views/analysis/AnalysisCenter.vue')
      },
      {
        path: 'analysis/r',
        name: 'RAnalysis',
        component: () => import('@/views/analysis/RAnalysis.vue')
      },
      {
        path: 'analysis/python',
        name: 'PythonAnalysis',
        component: () => import('@/views/analysis/PythonAnalysis.vue')
      },
      {
        path: 'analysis/tasks',
        name: 'AnalysisTasks',
        component: () => import('@/views/analysis/TaskList.vue')
      },
      {
        path: 'analysis/tasks/:id',
        name: 'TaskDetail',
        component: () => import('@/views/analysis/TaskDetail.vue'),
        props: true
      },
      {
        path: 'public-data',
        name: 'PublicData',
        component: () => import('@/views/public-data/Index.vue')
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/Index.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router