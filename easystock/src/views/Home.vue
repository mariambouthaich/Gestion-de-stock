<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-6 relative overflow-hidden" style="background: var(--surface-0)">
    <!-- Background decoration -->
    <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 h-96 w-96 rounded-full blur-3xl opacity-20" style="background: var(--accent)" />
      <div class="absolute bottom-1/4 right-1/4 h-64 w-64 rounded-full blur-3xl opacity-10" style="background: #7c3aed" />
    </div>

    <!-- Content -->
    <div class="relative z-10 text-center max-w-2xl">
      <!-- Logo -->
      <div class="inline-flex items-center justify-center h-20 w-20 rounded-3xl mb-8" style="background: var(--accent-dim); border: 1px solid var(--accent-glow)">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
          <polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/>
        </svg>
      </div>

      <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full mb-6 text-xs font-medium" style="background: var(--accent-dim); border: 1px solid var(--accent-glow); color: #a5b4fc">
        <span class="h-1.5 w-1.5 rounded-full" style="background: #a5b4fc" />
        Système de gestion des stocks
      </div>

      <h1 class="text-5xl font-bold tracking-tight mb-4" style="line-height: 1.1">
        EasyStock
      </h1>
      <p class="text-lg mb-10" style="color: var(--text-secondary)">
        Gérez vos produits, catégories, fournisseurs et mouvements de stock depuis une interface moderne et efficace.
      </p>

      <div class="flex flex-col sm:flex-row items-center justify-center gap-3">
        <router-link to="/login" class="btn-primary btn btn-lg">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 012 2v14a2 2 0 01-2 2h-4M10 17l5-5-5-5M15 12H3"/></svg>
          Accéder au dashboard
        </router-link>
        <router-link to="/dashboard" class="btn-ghost btn btn-lg">
          Explorer →
        </router-link>
      </div>

      <!-- Features -->
      <div class="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-4 text-left">
        <div v-for="f in features" :key="f.label" class="card p-4">
          <div class="h-8 w-8 rounded-lg flex items-center justify-center mb-3" style="background: var(--accent-dim)">
            <span v-html="f.icon" />
          </div>
          <div class="text-sm font-medium">{{ f.label }}</div>
          <div class="text-xs mt-1" style="color: var(--text-muted)">{{ f.desc }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const features = [
  {
    label: 'Produits',
    desc: 'CRUD complet',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>`
  },
  {
    label: 'Catégories',
    desc: 'Organisation',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>`
  },
  {
    label: 'Fournisseurs',
    desc: 'Gestion contacts',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>`
  },
  {
    label: 'Mouvements',
    desc: 'Historique stock',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>`
  },
]
</script>
