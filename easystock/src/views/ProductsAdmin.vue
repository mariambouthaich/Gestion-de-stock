<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex items-start justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Produits</h1>
        <p class="text-sm mt-1" style="color: var(--text-secondary)">
          {{ totalCount !== null ? `${totalCount} produit(s)` : 'Gestion du catalogue produits' }}
        </p>
      </div>
      <button class="btn-primary btn" @click="openCreate">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Nouveau produit
      </button>
    </div>

    <!-- Filters -->
    <div class="card p-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <input v-model.trim="filters.search" type="text" placeholder="Rechercher par nom..." class="input" @keydown.enter="applyFilters" />
        <select v-model="filters.categorie" class="input" @change="applyFilters">
          <option value="">Toutes les catégories</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.nom }}</option>
        </select>
        <select v-model="filters.fournisseur" class="input" @change="applyFilters">
          <option value="">Tous les fournisseurs</option>
          <option v-for="f in fournisseurs" :key="f.id" :value="f.id">{{ f.nom }}</option>
        </select>
        <div class="flex gap-2">
          <button class="btn-ghost btn flex-1" @click="resetFilters">Réinitialiser</button>
          <button class="btn-primary btn flex-1" :disabled="loading" @click="applyFilters">Filtrer</button>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-error">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      {{ error }}
      <button class="ml-auto underline text-xs" @click="error = null">✕</button>
    </div>

    <!-- Table -->
    <div class="card overflow-hidden">
      <LoadingSpinner v-if="loading" label="Chargement des produits..." />
      <div v-else>
        <EmptyState v-if="!items.length" title="Aucun produit" subtitle="Créez votre premier produit ou ajustez les filtres.">
          <button class="btn-primary btn mt-2" @click="openCreate">+ Créer un produit</button>
        </EmptyState>

        <div v-else class="overflow-x-auto">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Catégorie</th>
                <th>Fournisseur</th>
                <th>Prix</th>
                <th>Quantité</th>
                <th>Ajouté le</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in items" :key="p.id">
                <td><span class="badge badge-neutral font-mono">{{ p.id }}</span></td>
                <td>
                  <div class="font-medium">{{ p.nom }}</div>
                  <div v-if="p.description" class="text-xs mt-0.5 line-clamp-1" style="color: var(--text-muted)">{{ p.description }}</div>
                </td>
                <td>
                  <span v-if="p.categorie_nom" class="badge badge-accent">{{ p.categorie_nom }}</span>
                  <span v-else style="color: var(--text-muted)">—</span>
                </td>
                <td style="color: var(--text-secondary)">{{ p.fournisseur_nom || '—' }}</td>
                <td class="font-mono text-sm">{{ formatPrice(p.prix) }}</td>
                <td>
                  <span
                    class="badge"
                    :class="p.quantite === 0 ? 'badge-danger' : p.quantite < 5 ? 'badge-warn' : 'badge-success'"
                  >
                    {{ p.quantite === 0 ? '⚠ Rupture' : p.quantite < 5 ? `⚡ ${p.quantite}` : p.quantite }}
                  </span>
                </td>
                <td class="text-xs" style="color: var(--text-muted)">{{ formatDate(p.date_ajout) }}</td>
                <td class="text-right">
                  <div class="inline-flex items-center gap-2">
                    <button class="btn-ghost btn btn-sm" @click="openEdit(p)">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                      Modifier
                    </button>
                    <button class="btn-danger btn btn-sm" @click="askDelete(p)">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M19 6l-1 14H6L5 6M10 11v6M14 11v6M9 6V4h6v2"/></svg>
                      Supprimer
                    </button>
                  </div>
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

    <!-- Modal create/edit -->
    <Teleport to="body">
      <div v-if="modal.open" class="modal-overlay" @click.self="closeModal">
        <div class="modal-panel max-w-2xl max-h-[90vh] overflow-y-auto">
          <div class="flex items-start justify-between gap-4 mb-5">
            <div>
              <h2 class="text-lg font-bold">{{ modal.mode === 'create' ? 'Nouveau produit' : 'Modifier le produit' }}</h2>
              <p class="text-sm mt-0.5" style="color: var(--text-secondary)">Tous les champs marqués * sont requis.</p>
            </div>
            <button class="btn-ghost btn btn-sm flex-shrink-0" @click="closeModal">✕</button>
          </div>

          <div v-if="saveError" class="alert alert-error mb-4">{{ saveError }}</div>

          <form class="grid grid-cols-1 sm:grid-cols-2 gap-4" @submit.prevent="submit">
            <!-- Nom -->
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Nom <span style="color: var(--danger)">*</span></label>
              <input v-model.trim="form.nom" type="text" class="input" :class="formErrors.nom ? 'border-red-500/50' : ''" placeholder="Nom du produit" />
              <p v-if="formErrors.nom" class="mt-1 text-xs" style="color: var(--danger)">{{ formErrors.nom }}</p>
            </div>

            <!-- Description -->
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Description</label>
              <textarea v-model.trim="form.description" rows="2" class="input resize-none" placeholder="Description optionnelle..." />
            </div>

            <!-- Prix -->
            <div>
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Prix (€) <span style="color: var(--danger)">*</span></label>
              <input v-model.number="form.prix" type="number" step="0.01" min="0.01" class="input" :class="formErrors.prix ? 'border-red-500/50' : ''" />
              <p v-if="formErrors.prix" class="mt-1 text-xs" style="color: var(--danger)">{{ formErrors.prix }}</p>
            </div>

            <!-- Quantité -->
            <div>
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Quantité <span style="color: var(--danger)">*</span></label>
              <input v-model.number="form.quantite" type="number" min="0" class="input" :class="formErrors.quantite ? 'border-red-500/50' : ''" />
              <p v-if="formErrors.quantite" class="mt-1 text-xs" style="color: var(--danger)">{{ formErrors.quantite }}</p>
            </div>

            <!-- Catégorie -->
            <div>
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Catégorie</label>
              <select v-model="form.categorie" class="input">
                <option :value="null">— Aucune —</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.nom }}</option>
              </select>
            </div>

            <!-- Fournisseur -->
            <div>
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Fournisseur</label>
              <select v-model="form.fournisseur" class="input">
                <option :value="null">— Aucun —</option>
                <option v-for="f in fournisseurs" :key="f.id" :value="f.id">{{ f.nom }}</option>
              </select>
            </div>

            <div class="sm:col-span-2 flex justify-end gap-2 pt-1">
              <button type="button" class="btn-ghost btn" @click="closeModal">Annuler</button>
              <button type="submit" class="btn-primary btn" :disabled="saving">
                <svg v-if="saving" class="animate-spin" width="14" height="14" viewBox="0 0 24 24" fill="none"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/></svg>
                {{ saving ? 'Enregistrement...' : modal.mode === 'create' ? 'Créer' : 'Mettre à jour' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <ConfirmModal
      :open="deleteModal.open"
      :title="`Supprimer &quot;${deleteModal.item?.nom}&quot; ?`"
      message="Ce produit sera supprimé définitivement et ses mouvements de stock seront perdus."
      :loading="deleteModal.loading"
      @confirm="doDelete"
      @cancel="deleteModal.open = false"
    />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import LoadingSpinner from '../components/ui/LoadingSpinner.vue'
import Pagination from '../components/ui/Pagination.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import ConfirmModal from '../components/ui/ConfirmModal.vue'
import { listProducts, createProduct, updateProduct, deleteProduct } from '../services/products'
import { listCategories } from '../services/categories'
import { listSuppliers } from '../services/suppliers'

const loading = ref(false), error = ref(null)
const items = ref([]), page = ref(1), totalPages = ref(1), totalCount = ref(null)
const categories = ref([]), fournisseurs = ref([])

const filters = reactive({ search: '', categorie: '', fournisseur: '' })
const activeFilters = reactive({ search: '', categorie: '', fournisseur: '' })

const modal = reactive({ open: false, mode: 'create' })
const form = reactive({ id: null, nom: '', description: '', prix: 0, quantite: 0, categorie: null, fournisseur: null })
const formErrors = reactive({ nom: '', prix: '', quantite: '' })
const saving = ref(false), saveError = ref(null)
const deleteModal = reactive({ open: false, item: null, loading: false })

// ── Helpers ───────────────────────────────────────────────────────────────
function formatPrice(v) {
  if (v === null || v === undefined) return '—'
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(Number(v))
}
function formatDate(v) {
  if (!v) return '—'
  return new Date(v).toLocaleDateString('fr-FR')
}

// ── Fetch ─────────────────────────────────────────────────────────────────
async function fetchLookups() {
  try {
    const [catRes, supRes] = await Promise.all([
      listCategories({ page_size: 200 }),
      listSuppliers({ page_size: 200 })
    ])
    const catData = catRes?.data ?? catRes
    const supData = supRes?.data ?? supRes
    categories.value  = Array.isArray(catData) ? catData : catData?.results || []
    fournisseurs.value = Array.isArray(supData) ? supData : supData?.results || []
  } catch { /* non-blocking */ }
}

async function fetchData() {
  loading.value = true; error.value = null
  try {
    const params = { page: page.value, page_size: 10 }
    if (activeFilters.search) params.search = activeFilters.search
    if (activeFilters.categorie) params.categorie = activeFilters.categorie
    if (activeFilters.fournisseur) params.fournisseur = activeFilters.fournisseur
    const res = await listProducts(params)
    const data = res?.data ?? res
    if (Array.isArray(data)) {
      items.value = data; totalPages.value = 1; totalCount.value = data.length
    } else {
      items.value = data.results || []
      totalCount.value = data.count ?? items.value.length
      totalPages.value = Math.ceil(totalCount.value / 10) || 1
    }
  } catch (e) { error.value = e?.message || 'Erreur de chargement.' }
  finally { loading.value = false }
}

function applyFilters() {
  Object.assign(activeFilters, { search: filters.search, categorie: filters.categorie, fournisseur: filters.fournisseur })
  page.value = 1; fetchData()
}
function resetFilters() {
  Object.assign(filters, { search: '', categorie: '', fournisseur: '' })
  Object.assign(activeFilters, { search: '', categorie: '', fournisseur: '' })
  page.value = 1; fetchData()
}
function onPageChange(p) { page.value = p; fetchData() }

// ── Modal ─────────────────────────────────────────────────────────────────
function openCreate() {
  modal.mode = 'create'
  Object.assign(form, { id: null, nom: '', description: '', prix: 0, quantite: 0, categorie: null, fournisseur: null })
  Object.assign(formErrors, { nom: '', prix: '', quantite: '' })
  saveError.value = null; modal.open = true
}
function openEdit(p) {
  modal.mode = 'edit'
  Object.assign(form, { id: p.id, nom: p.nom, description: p.description || '', prix: Number(p.prix ?? 0), quantite: Number(p.quantite ?? 0), categorie: p.categorie ?? null, fournisseur: p.fournisseur ?? null })
  Object.assign(formErrors, { nom: '', prix: '', quantite: '' })
  saveError.value = null; modal.open = true
}
function closeModal() { modal.open = false }

function validate() {
  let ok = true
  formErrors.nom = formErrors.prix = formErrors.quantite = ''
  if (!form.nom || form.nom.length < 2) { formErrors.nom = 'Nom requis (min 2 car.).'; ok = false }
  if (!form.prix || Number(form.prix) <= 0) { formErrors.prix = 'Prix doit être > 0.'; ok = false }
  if (form.quantite === null || form.quantite < 0) { formErrors.quantite = 'Quantité doit être ≥ 0.'; ok = false }
  return ok
}

async function submit() {
  if (!validate()) return
  saving.value = true; saveError.value = null
  try {
    const payload = { nom: form.nom, description: form.description, prix: form.prix, quantite: form.quantite, categorie: form.categorie, fournisseur: form.fournisseur }
    if (modal.mode === 'create') await createProduct(payload)
    else await updateProduct(form.id, payload)
    closeModal(); await fetchData()
  } catch (e) { saveError.value = e?.message || 'Erreur lors de l\'enregistrement.' }
  finally { saving.value = false }
}

// ── Delete ────────────────────────────────────────────────────────────────
function askDelete(p) { deleteModal.item = p; deleteModal.open = true; deleteModal.loading = false }
async function doDelete() {
  deleteModal.loading = true
  try {
    await deleteProduct(deleteModal.item.id)
    deleteModal.open = false
    if (items.value.length === 1 && page.value > 1) page.value--
    await fetchData()
  } catch (e) { error.value = e?.message || 'Erreur de suppression.'; deleteModal.open = false }
  finally { deleteModal.loading = false }
}

onMounted(async () => { await fetchLookups(); await fetchData() })
</script>
