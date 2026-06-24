<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Vue d'ensemble</h1>
      <p class="text-sm mt-1" style="color: var(--text-secondary)">Indicateurs clés et activité récente.</p>
    </div>

    <!-- Alerts banner -->
    <div v-if="!loading && stats && (stats.produits_rupture > 0 || stats.produits_stock_faible > 0)" class="flex flex-col sm:flex-row gap-3">
      <div v-if="stats.produits_rupture > 0" class="alert alert-error flex-1">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <span><strong>{{ stats.produits_rupture }}</strong> produit(s) en rupture de stock</span>
      </div>
      <div v-if="stats.produits_stock_faible > 0" class="alert flex-1" style="background: var(--warn-dim); border: 1px solid rgba(251,191,36,0.2); color: var(--warn)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <span><strong>{{ stats.produits_stock_faible }}</strong> produit(s) à stock faible (≤4)</span>
      </div>
    </div>

    <!-- KPI Cards skeleton -->
    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div v-for="i in 7" :key="i" class="stat-card h-28 animate-pulse" style="background: rgba(255,255,255,0.03)" />
    </div>

    <!-- KPI Cards -->
    <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      <div v-for="kpi in kpiCards" :key="kpi.label" class="stat-card">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium uppercase tracking-wider" style="color: var(--text-muted)">{{ kpi.label }}</span>
          <div class="h-8 w-8 rounded-lg flex items-center justify-center" :style="{ background: kpi.iconBg || 'var(--accent-dim)' }" v-html="kpi.icon" />
        </div>
        <div class="text-3xl font-bold tracking-tight mt-3" :style="{ color: kpi.valueColor || 'var(--text-primary)' }">
          {{ kpi.value ?? '—' }}
        </div>
        <div class="text-xs mt-1" style="color: var(--text-muted)">{{ kpi.subtitle }}</div>
      </div>
    </div>

    <!-- Tables section -->
    <div v-if="!loading && stats" class="grid gap-6 lg:grid-cols-2">
      <!-- Top products -->
      <div class="card p-5">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="font-semibold text-sm">Top produits en stock</h2>
            <p class="text-xs mt-0.5" style="color: var(--text-muted)">Quantités les plus élevées</p>
          </div>
          <router-link :to="{ name: 'dashboard-products' }" class="text-xs btn-ghost btn btn-sm">Voir tout →</router-link>
        </div>

        <div v-if="!stats.top_produits_en_stock?.length" class="py-6 text-center text-xs" style="color: var(--text-muted)">
          Aucune donnée disponible.
        </div>
        <ul v-else class="space-y-2">
          <li
            v-for="(p, i) in stats.top_produits_en_stock"
            :key="p.nom"
            class="flex items-center gap-3 py-2 px-3 rounded-xl"
            style="background: rgba(255,255,255,0.02)"
          >
            <span class="h-6 w-6 rounded-lg flex items-center justify-center text-xs font-bold flex-shrink-0" style="background: var(--accent-dim); color: #a5b4fc">
              {{ i + 1 }}
            </span>
            <span class="flex-1 text-sm truncate">{{ p.nom }}</span>
            <span class="badge badge-accent font-mono">{{ p.quantite }}</span>
          </li>
        </ul>
      </div>

      <!-- Category breakdown -->
      <div class="card p-5">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="font-semibold text-sm">Répartition par catégorie</h2>
            <p class="text-xs mt-0.5" style="color: var(--text-muted)">Nombre de produits par catégorie</p>
          </div>
          <router-link :to="{ name: 'dashboard-categories' }" class="text-xs btn-ghost btn btn-sm">Gérer →</router-link>
        </div>

        <div v-if="!stats.repartition_par_categorie?.length" class="py-6 text-center text-xs" style="color: var(--text-muted)">
          Aucune catégorie.
        </div>
        <ul v-else class="space-y-2">
          <li
            v-for="c in stats.repartition_par_categorie"
            :key="c.nom"
            class="flex items-center gap-3 py-2 px-3 rounded-xl"
            style="background: rgba(255,255,255,0.02)"
          >
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm truncate">{{ c.nom }}</span>
                <span class="text-xs font-medium" style="color: var(--text-muted)">{{ c.nb_produits }}</span>
              </div>
              <!-- Mini progress bar -->
              <div class="h-1.5 rounded-full overflow-hidden" style="background: rgba(255,255,255,0.06)">
                <div
                  class="h-full rounded-full transition-all duration-500"
                  style="background: var(--accent)"
                  :style="{ width: barWidth(c.nb_produits) }"
                />
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Quick links -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
      <router-link
        v-for="link in quickLinks"
        :key="link.name"
        :to="{ name: link.name }"
        class="card p-4 flex items-center gap-3 transition-all duration-200 hover:no-underline"
        style="text-decoration: none"
      >
        <div class="h-9 w-9 rounded-xl flex items-center justify-center flex-shrink-0" style="background: var(--accent-dim)">
          <span v-html="link.icon" />
        </div>
        <div class="min-w-0">
          <div class="text-sm font-medium truncate">{{ link.label }}</div>
          <div class="text-xs mt-0.5 truncate" style="color: var(--text-muted)">{{ link.desc }}</div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getDashboardStats } from '../services/stats'

const loading = ref(true)
const stats   = ref(null)

function fmt(v) {
  if (v === null || v === undefined) return '—'
  return new Intl.NumberFormat('fr-FR').format(Number(v))
}
function fmtMoney(v) {
  if (v === null || v === undefined) return '—'
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(Number(v))
}

const kpiCards = computed(() => {
  if (!stats.value) return []
  return [
    {
      label: 'Produits',
      value: fmt(stats.value.total_produits),
      subtitle: 'références en catalogue',
      icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>`,
    },
    {
      label: 'Catégories',
      value: fmt(stats.value.total_categories),
      subtitle: 'catégories actives',
      icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>`,
    },
    {
      label: 'Fournisseurs',
      value: fmt(stats.value.total_fournisseurs),
      subtitle: 'partenaires actifs',
      icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>`,
    },
    {
      label: 'Valeur du stock',
      value: fmtMoney(stats.value.valeur_totale_stock),
      subtitle: 'valeur totale estimée',
      icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>`,
    },
    {
      label: 'Stock faible',
      value: fmt(stats.value.produits_stock_faible),
      subtitle: 'produits (quantité 1-4)',
      valueColor: stats.value.produits_stock_faible > 0 ? 'var(--warn)' : undefined,
      iconBg: stats.value.produits_stock_faible > 0 ? 'var(--warn-dim)' : undefined,
      icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="${stats.value.produits_stock_faible > 0 ? '#fbbf24' : '#a5b4fc'}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
    },
    {
      label: 'Rupture de stock',
      value: fmt(stats.value.produits_rupture),
      subtitle: 'produits (quantité 0)',
      valueColor: stats.value.produits_rupture > 0 ? 'var(--danger)' : undefined,
      iconBg: stats.value.produits_rupture > 0 ? 'var(--danger-dim)' : undefined,
      icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="${stats.value.produits_rupture > 0 ? '#f87171' : '#a5b4fc'}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
    },
    {
      label: 'Mouvements (7j)',
      value: fmt(stats.value.mouvements_7_derniers_jours),
      subtitle: 'opérations cette semaine',
      icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>`,
    },
  ]
})

const maxProduits = computed(() => {
  const reps = stats.value?.repartition_par_categorie || []
  return Math.max(...reps.map(c => c.nb_produits), 1)
})

function barWidth(n) {
  return `${Math.round((n / maxProduits.value) * 100)}%`
}

const quickLinks = [
  { name: 'dashboard-products',   label: 'Ajouter produit',    desc: 'Nouveau produit',    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>` },
  { name: 'dashboard-categories', label: 'Catégories',         desc: 'Gérer les catégories', icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg>` },
  { name: 'dashboard-suppliers',  label: 'Fournisseurs',       desc: 'Gérer les fournisseurs', icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>` },
  { name: 'dashboard-stock',      label: 'Mouvements',         desc: 'Historique du stock',  icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="2" stroke-linecap="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/></svg>` },
]

async function load() {
  loading.value = true
  try {
    const res = await getDashboardStats()
    stats.value = res?.data ?? res
  } catch {
    stats.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
