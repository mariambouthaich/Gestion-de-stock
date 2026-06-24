<template>
  <div class="space-y-6 animate-fade-in">
    <div class="flex items-start justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Mouvements de stock</h1>
        <p class="text-sm mt-1" style="color: var(--text-secondary)">
          {{ totalCount !== null ? `${totalCount} mouvement(s)` : 'Historique des entrées et sorties de stock' }}
        </p>
      </div>
    </div>

    <!-- Filters -->
    <div class="card p-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <select v-model="filters.type" class="input" @change="applyFilters">
          <option value="">Tous les types</option>
          <option value="ajout">Ajout</option>
          <option value="retrait">Retrait</option>
          <option value="modification">Modification</option>
        </select>
        <input v-model="filters.dateDebut" type="date" class="input" @change="applyFilters" />
        <input v-model="filters.dateFin" type="date" class="input" @change="applyFilters" />
        <div class="flex gap-2">
          <button class="btn-ghost btn flex-1" @click="resetFilters">Réinitialiser</button>
          <button class="btn-primary btn flex-1" :disabled="loading" @click="applyFilters">Filtrer</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-error">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      {{ error }}
      <button class="ml-auto underline text-xs" @click="error = null">✕</button>
    </div>

    <div class="card overflow-hidden">
      <LoadingSpinner v-if="loading" label="Chargement des mouvements..." />
      <div v-else>
        <EmptyState v-if="!items.length" title="Aucun mouvement" subtitle="Les mouvements de stock apparaîtront ici lors de créations ou modifications de produits." />
        <div v-else class="overflow-x-auto">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Produit</th>
                <th>Type</th>
                <th>Quantité</th>
                <th>Utilisateur</th>
                <th>Date</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in items" :key="m.id">
                <td><span class="badge badge-neutral font-mono">{{ m.id }}</span></td>
                <td class="font-medium">{{ m.produit_nom || '—' }}</td>
                <td>
                  <span class="badge" :class="typeBadge(m.type_mouvement)">
                    {{ typeLabel(m.type_mouvement) }}
                  </span>
                </td>
                <td class="font-mono font-medium">{{ m.quantite }}</td>
                <td style="color: var(--text-secondary)">{{ m.utilisateur_nom || '—' }}</td>
                <td class="text-xs" style="color: var(--text-secondary)">{{ formatDate(m.date) }}</td>
                <td style="color: var(--text-muted); max-width: 200px">
                  <span class="line-clamp-1">{{ m.note || '—' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="px-4">
          <Pagination :page="page" :total-pages="totalPages" :total-count="totalCount" :loading="loading" @change="onPageChange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import LoadingSpinner from '../components/ui/LoadingSpinner.vue'
import Pagination from '../components/ui/Pagination.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import { listStockMovements } from '../services/stockMovements'

const loading = ref(false), error = ref(null)
const items = ref([]), page = ref(1), totalPages = ref(1), totalCount = ref(null)
const filters = reactive({ type: '', dateDebut: '', dateFin: '' })
const activeFilters = reactive({ type: '', dateDebut: '', dateFin: '' })

function typeBadge(t) {
  if (t === 'ajout') return 'badge-success'
  if (t === 'retrait') return 'badge-danger'
  return 'badge-neutral'
}
function typeLabel(t) {
  return { ajout: '↑ Ajout', retrait: '↓ Retrait', modification: '~ Modification' }[t] || t
}
function formatDate(v) {
  if (!v) return '—'
  return new Date(v).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' })
}

async function fetchData() {
  loading.value = true; error.value = null
  try {
    const params = { page: page.value, page_size: 15 }
    if (activeFilters.type) params.type = activeFilters.type
    if (activeFilters.dateDebut) params.date_debut = activeFilters.dateDebut
    if (activeFilters.dateFin) params.date_fin = activeFilters.dateFin
    const res = await listStockMovements(params)
    const data = res?.data ?? res
    if (Array.isArray(data)) {
      items.value = data; totalPages.value = 1; totalCount.value = data.length
    } else {
      items.value = data.results || []
      totalCount.value = data.count ?? items.value.length
      totalPages.value = Math.ceil(totalCount.value / 15) || 1
    }
  } catch (e) { error.value = e?.message || 'Erreur de chargement.' }
  finally { loading.value = false }
}

function applyFilters() { Object.assign(activeFilters, filters); page.value = 1; fetchData() }
function resetFilters() {
  Object.assign(filters, { type: '', dateDebut: '', dateFin: '' })
  Object.assign(activeFilters, { type: '', dateDebut: '', dateFin: '' })
  page.value = 1; fetchData()
}
function onPageChange(p) { page.value = p; fetchData() }

onMounted(fetchData)
</script>
