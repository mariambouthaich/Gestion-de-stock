<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden" style="background: var(--surface-0)">
    <!-- Glow -->
    <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 h-96 w-96 rounded-full blur-3xl opacity-15" style="background: var(--accent)" />
    </div>

    <div class="relative z-10 w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center h-16 w-16 rounded-2xl mb-5" style="background: var(--accent-dim); border: 1px solid var(--accent-glow)">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
            <polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold">Connexion</h1>
        <p class="text-sm mt-1" style="color: var(--text-secondary)">Accédez à votre espace de gestion</p>
      </div>

      <!-- Card -->
      <div class="card p-7" style="background: var(--surface-1)">
        <!-- Alert -->
        <div v-if="alert" :class="['alert mb-5', alert.type === 'error' ? 'alert-error' : 'alert-success']">
          <svg v-if="alert.type === 'error'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
          <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          <span>{{ alert.message }}</span>
        </div>

        <form class="space-y-4" @submit.prevent="onSubmit">
          <!-- Username -->
          <div>
            <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">
              Nom d'utilisateur
            </label>
            <input
              v-model.trim="form.username"
              type="text"
              autocomplete="username"
              class="input"
              :class="errors.username ? 'border-red-500/50' : ''"
              placeholder="admin"
            />
            <p v-if="errors.username" class="mt-1 text-xs" style="color: var(--danger)">{{ errors.username }}</p>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">
              Mot de passe
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPwd ? 'text' : 'password'"
                autocomplete="current-password"
                class="input pr-10"
                :class="errors.password ? 'border-red-500/50' : ''"
                placeholder="••••••••"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2"
                style="color: var(--text-muted)"
                @click="showPwd = !showPwd"
              >
                <svg v-if="!showPwd" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24M1 1l22 22"/></svg>
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-xs" style="color: var(--danger)">{{ errors.password }}</p>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            class="btn-primary btn w-full mt-2"
            style="padding-top: 10px; padding-bottom: 10px"
            :disabled="loading"
          >
            <svg v-if="loading" class="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
            </svg>
            {{ loading ? 'Connexion...' : 'Se connecter' }}
          </button>
        </form>

        <p class="text-center text-xs mt-5" style="color: var(--text-muted)">
          Authentification sécurisée par JWT
        </p>
      </div>

      <p class="text-center text-xs mt-4" style="color: var(--text-muted)">
        <router-link to="/" style="color: var(--text-secondary)">← Retour à l'accueil</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../services/auth'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const errors = reactive({ username: '', password: '' })
const loading = ref(false)
const showPwd = ref(false)
const alert = ref(null)

function validate() {
  errors.username = ''
  errors.password = ''
  let ok = true
  if (!form.username) { errors.username = 'Nom d\'utilisateur requis.'; ok = false }
  if (!form.password) { errors.password = 'Mot de passe requis.'; ok = false }
  else if (form.password.length < 4) { errors.password = 'Mot de passe trop court.'; ok = false }
  return ok
}

async function onSubmit() {
  alert.value = null
  if (!validate()) return
  
  loading.value = true
  try {
    await login({ username: form.username, password: form.password })
    alert.value = { type: 'success', message: 'Connexion réussie. Redirection...' }
    setTimeout(() => router.push({ name: 'dashboard-home' }), 400)
  } catch (e) {
    alert.value = { type: 'error', message: e?.message || 'Identifiants incorrects.' }
  } finally {
    loading.value = false
  }
}
</script>
