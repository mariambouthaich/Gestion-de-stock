import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../services/auth'

// Lazy-loaded views
const Home         = () => import('../views/Home.vue')
const Login        = () => import('../views/Login.vue')
const DashLayout   = () => import('../components/DashboardLayout.vue')
const Dashboard    = () => import('../views/Dashboard.vue')
const Products     = () => import('../views/ProductsAdmin.vue')
const Categories   = () => import('../views/Categories.vue')
const Suppliers    = () => import('../views/Suppliers.vue')
const Stock        = () => import('../views/Stock.vue')
const Users        = () => import('../views/Users.vue')
const Settings     = () => import('../views/Settings.vue')

const requireAuth = () => {
  if (!isAuthenticated()) return { name: 'login' }
}

export function makeRouter() {
  return createRouter({
    history: createWebHistory(),
    scrollBehavior: () => ({ top: 0 }),
    routes: [
      { path: '/', name: 'home', component: Home },
      { path: '/login', name: 'login', component: Login },
      {
        path: '/dashboard',
        name: 'dashboard',
        component: DashLayout,
        beforeEnter: requireAuth,
        children: [
          { path: '',        name: 'dashboard-home',       component: Dashboard },
          { path: 'products',name: 'dashboard-products',   component: Products,    beforeEnter: requireAuth },
          { path: 'categories', name: 'dashboard-categories', component: Categories, beforeEnter: requireAuth },
          { path: 'suppliers',  name: 'dashboard-suppliers',  component: Suppliers,  beforeEnter: requireAuth },
          { path: 'stock',      name: 'dashboard-stock',      component: Stock,      beforeEnter: requireAuth },
          { path: 'users',      name: 'dashboard-users',      component: Users,      beforeEnter: requireAuth },
          { path: 'settings',   name: 'dashboard-settings',   component: Settings,   beforeEnter: requireAuth },
        ]
      },
      {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: {
          template: `
            <div class="flex flex-col items-center justify-center min-h-[60vh] gap-4 text-center">
              <div class="text-7xl font-bold text-brand-500/30">404</div>
              <h1 class="text-2xl font-semibold">Page introuvable</h1>
              <p class="text-sm" style="color: var(--text-secondary)">La page que vous cherchez n'existe pas.</p>
              <router-link to="/dashboard" class="btn-primary btn mt-2">Retour au dashboard</router-link>
            </div>
          `
        }
      }
    ]
  })
}
