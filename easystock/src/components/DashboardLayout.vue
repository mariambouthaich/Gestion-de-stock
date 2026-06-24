<template>
  <div class="min-h-screen flex" style="background: var(--surface-0)">

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-30 flex flex-col transition-all duration-300"
      :class="sidebarCollapsed ? 'w-16' : 'w-60'"
      style="background: var(--surface-1); border-right: 1px solid var(--border)"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-4 py-5" :class="sidebarCollapsed ? 'justify-center' : ''">
        <div class="flex-shrink-0 h-9 w-9 rounded-xl flex items-center justify-center" style="background: var(--accent-dim); border: 1px solid var(--accent-glow)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
            <polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/>
          </svg>
        </div>
        <div v-if="!sidebarCollapsed" class="min-w-0">
          <div class="font-bold text-sm leading-tight truncate">EasyStock</div>
          <div class="text-xs truncate" style="color: var(--text-muted)">Inventory System</div>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-2 pb-4 space-y-1 overflow-y-auto">
        <div v-if="!sidebarCollapsed" class="px-2 pt-2 pb-1">
          <span class="text-[10px] font-semibold uppercase tracking-widest" style="color: var(--text-muted)">Navigation</span>
        </div>

        <router-link
          v-for="item in navItems"
          :key="item.name"
          :to="{ name: item.name }"
          class="nav-item group"
          :class="[
            isActive(item.name) ? 'active' : '',
            sidebarCollapsed ? 'justify-center px-0' : ''
          ]"
          :title="sidebarCollapsed ? item.label : ''"
        >
          <span class="flex-shrink-0" v-html="item.icon" />
          <span v-if="!sidebarCollapsed" class="truncate">{{ item.label }}</span>
          <!-- Tooltip when collapsed -->
          <div
            v-if="sidebarCollapsed"
            class="absolute left-full ml-3 px-2.5 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-50"
            style="background: var(--surface-3); border: 1px solid var(--border); color: var(--text-primary)"
          >
            {{ item.label }}
          </div>
        </router-link>
      </nav>

      <!-- User + collapse -->
      <div class="px-2 pb-4 space-y-2" style="border-top: 1px solid var(--border); padding-top: 12px; margin-top: 8px">
        <!-- User -->
        <div
          v-if="user && !sidebarCollapsed"
          class="flex items-center gap-3 px-3 py-2.5 rounded-xl"
          style="background: rgba(255,255,255,0.03)"
        >
          <div class="h-7 w-7 rounded-lg flex items-center justify-center text-xs font-bold flex-shrink-0" style="background: var(--accent-dim); color: #a5b4fc">
            {{ userInitial }}
          </div>
          <div class="min-w-0 flex-1">
            <div class="text-xs font-medium truncate">{{ user.username }}</div>
            <div class="text-[10px] truncate" style="color: var(--text-muted)">{{ user.is_staff ? 'Admin' : 'Utilisateur' }}</div>
          </div>
        </div>

        <!-- Collapse toggle -->
        <button
          class="nav-item w-full"
          :class="sidebarCollapsed ? 'justify-center px-0' : ''"
          @click="sidebarCollapsed = !sidebarCollapsed"
        >
          <svg
            width="16" height="16" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="transition-transform duration-300"
            :class="sidebarCollapsed ? 'rotate-180' : ''"
          >
            <path d="M11 17l-5-5 5-5M18 17l-5-5 5-5"/>
          </svg>
          <span v-if="!sidebarCollapsed" class="text-sm">Réduire</span>
        </button>

        <!-- Logout -->
        <button
          class="nav-item w-full text-sm"
          :class="sidebarCollapsed ? 'justify-center px-0' : ''"
          style="color: #f87171"
          @click="handleLogout"
          :title="sidebarCollapsed ? 'Se déconnecter' : ''"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
          </svg>
          <span v-if="!sidebarCollapsed">Déconnexion</span>
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col min-w-0 transition-all duration-300" :style="{ marginLeft: sidebarCollapsed ? '64px' : '240px' }">

      <!-- Top bar -->
      <header class="sticky top-0 z-20 flex items-center justify-between gap-4 px-6 h-14" style="background: rgba(8,12,24,0.85); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border)">
        <!-- Breadcrumb -->
        <div class="flex items-center gap-2 text-sm min-w-0">
          <span style="color: var(--text-muted)">EasyStock</span>
          <span style="color: var(--text-muted)">/</span>
          <span class="font-medium truncate">{{ currentPageLabel }}</span>
        </div>

        <!-- Right side -->
        <div class="flex items-center gap-3 flex-shrink-0">
          <!-- Mobile menu button -->
          <button
            class="md:hidden btn-ghost btn btn-sm"
            @click="mobileOpen = !mobileOpen"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
          </button>
        </div>
      </header>

      <!-- Mobile drawer overlay -->
      <div v-if="mobileOpen" class="fixed inset-0 z-40 bg-black/60 md:hidden" @click="mobileOpen = false" />
      <div
        v-if="mobileOpen"
        class="fixed left-0 top-0 bottom-0 z-50 w-64 flex flex-col md:hidden"
        style="background: var(--surface-1); border-right: 1px solid var(--border)"
      >
        <div class="flex items-center justify-between px-4 py-4" style="border-bottom: 1px solid var(--border)">
          <span class="font-bold">EasyStock</span>
          <button class="btn-ghost btn btn-sm" @click="mobileOpen = false">✕</button>
        </div>
        <nav class="flex-1 px-2 py-3 space-y-1 overflow-y-auto">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="{ name: item.name }"
            class="nav-item"
            :class="isActive(item.name) ? 'active' : ''"
            @click="mobileOpen = false"
          >
            <span v-html="item.icon" />
            {{ item.label }}
          </router-link>
        </nav>
        <div class="px-2 pb-4 pt-3" style="border-top: 1px solid var(--border)">
          <button class="nav-item w-full" style="color: #f87171" @click="handleLogout">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
            </svg>
            Déconnexion
          </button>
        </div>
      </div>

      <!-- Page content -->
      <main class="flex-1 p-6 overflow-auto">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { logout, getUser } from '../services/auth'

const route = useRoute()
const router = useRouter()
const sidebarCollapsed = ref(false)
const mobileOpen = ref(false)

const user = computed(() => getUser())
const userInitial = computed(() => (user.value?.username?.[0] || 'U').toUpperCase())

const navItems = [
  {
    name: 'dashboard-home',
    label: 'Vue d\'ensemble',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`
  },
  {
    name: 'dashboard-products',
    label: 'Produits',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>`
  },
  {
    name: 'dashboard-categories',
    label: 'Catégories',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>`
  },
  {
    name: 'dashboard-suppliers',
    label: 'Fournisseurs',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>`
  },
  {
    name: 'dashboard-stock',
    label: 'Mouvements',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>`
  },
  {
    name: 'dashboard-users',
    label: 'Utilisateurs',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`
  },
  {
    name: 'dashboard-settings',
    label: 'Paramètres',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93l-1.41 1.41M12 2v2M4.93 4.93l1.41 1.41M2 12h2M4.93 19.07l1.41-1.41M12 22v-2M19.07 19.07l-1.41-1.41M22 12h-2"/></svg>`
  },
]

const pageLabels = {
  'dashboard-home':       'Vue d\'ensemble',
  'dashboard-products':   'Produits',
  'dashboard-categories': 'Catégories',
  'dashboard-suppliers':  'Fournisseurs',
  'dashboard-stock':      'Mouvements de stock',
  'dashboard-users':      'Utilisateurs',
  'dashboard-settings':   'Paramètres',
}

const currentPageLabel = computed(() => pageLabels[route.name] || 'Dashboard')

function isActive(name) {
  return route.name === name
}

function handleLogout() {
  logout()
  router.push({ name: 'login' })
}
</script>
