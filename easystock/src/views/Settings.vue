<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Paramètres</h1>
      <p class="text-sm mt-1" style="color: var(--text-secondary)">Configuration de l'application EasyStock.</p>
    </div>

    <!-- API Config -->
    <div class="card p-6 space-y-4">
      <h2 class="font-semibold text-base">Configuration API</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-medium mb-1.5" style="color: var(--text-muted)">URL de base</label>
          <div class="input font-mono text-xs" style="color: var(--text-secondary)">{{ apiBase }}</div>
        </div>
        <div>
          <label class="block text-xs font-medium mb-1.5" style="color: var(--text-muted)">Endpoint Auth</label>
          <div class="input font-mono text-xs" style="color: var(--text-secondary)">{{ authEndpoint }}</div>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <div class="h-2 w-2 rounded-full" :class="apiStatus === 'ok' ? 'bg-green-400' : apiStatus === 'checking' ? 'bg-yellow-400 animate-pulse' : 'bg-red-400'" />
        <span class="text-xs" style="color: var(--text-secondary)">
          {{ apiStatus === 'ok' ? 'Backend accessible' : apiStatus === 'checking' ? 'Vérification...' : 'Backend inaccessible' }}
        </span>
        <button class="btn-ghost btn btn-sm ml-2" @click="checkApi">Tester</button>
      </div>
    </div>

    <!-- Session -->
    <div class="card p-6 space-y-4">
      <h2 class="font-semibold text-base">Session</h2>
      <div class="flex items-center justify-between p-4 rounded-xl" style="background: rgba(255,255,255,0.03)">
        <div>
          <div class="text-sm font-medium">{{ user?.username || '—' }}</div>
          <div class="text-xs mt-0.5" style="color: var(--text-muted)">{{ user?.is_staff ? 'Administrateur' : 'Utilisateur' }}</div>
        </div>
        <button class="btn-danger btn btn-sm" @click="handleLogout">Déconnexion</button>
      </div>
    </div>

    <!-- About -->
    <div class="card p-6">
      <h2 class="font-semibold text-base mb-3">À propos</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
        <div class="p-3 rounded-xl" style="background: rgba(255,255,255,0.03)">
          <div class="text-xs" style="color: var(--text-muted)">Frontend</div>
          <div class="font-medium text-sm mt-1">Vue 3</div>
        </div>
        <div class="p-3 rounded-xl" style="background: rgba(255,255,255,0.03)">
          <div class="text-xs" style="color: var(--text-muted)">Backend</div>
          <div class="font-medium text-sm mt-1">Django REST</div>
        </div>
        <div class="p-3 rounded-xl" style="background: rgba(255,255,255,0.03)">
          <div class="text-xs" style="color: var(--text-muted)">Auth</div>
          <div class="font-medium text-sm mt-1">JWT</div>
        </div>
        <div class="p-3 rounded-xl" style="background: rgba(255,255,255,0.03)">
          <div class="text-xs" style="color: var(--text-muted)">Version</div>
          <div class="font-medium text-sm mt-1">1.0.0</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { logout, getUser } from '../services/auth'
import { getDashboardStats } from '../services/stats'

const router = useRouter()
const user = getUser()
const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const authEndpoint = import.meta.env.VITE_AUTH_ENDPOINT || '/api/login/'
const apiStatus = ref('idle')

async function checkApi() {
  apiStatus.value = 'checking'
  try { await getDashboardStats(); apiStatus.value = 'ok' }
  catch { apiStatus.value = 'error' }
}

function handleLogout() { logout(); router.push({ name: 'login' }) }
</script>
