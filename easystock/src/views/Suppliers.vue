<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Header -->
    <div class="flex items-start justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Fournisseurs</h1>
        <p class="text-sm mt-1" style="color: var(--text-secondary)">
          {{ totalCount !== null ? `${totalCount} fournisseur(s)` : 'Gestion des fournisseurs' }}
        </p>
      </div>
      <button class="btn-primary btn" @click="openCreate">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Nouveau fournisseur
      </button>
    </div>

    <!-- Toolbar -->
    <div class="card p-4">
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model.trim="search" type="text" placeholder="Filtrer par nom..." class="input flex-1" @keydown.enter="applySearch" />
        <div class="flex gap-2">
          <button class="btn-ghost btn" :disabled="!search" @click="clearSearch">Effacer</button>
          <button class="btn-primary btn" :disabled="loading" @click="applySearch">Rechercher</button>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-error">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      {{ error }}
      <button class="ml-auto underline text-xs" @click="error = null">✕</button>
    </div>

    <!-- Table card -->
    <div class="card overflow-hidden">
      <LoadingSpinner v-if="loading" label="Chargement..." />
      <div v-else>
        <EmptyState v-if="!items.length" title="Aucun fournisseur" subtitle="Créez votre premier fournisseur.">
          <button class="btn-primary btn mt-2" @click="openCreate">+ Créer</button>
        </EmptyState>

        <div v-else class="overflow-x-auto">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Email</th>
                <th>Téléphone</th>
                <th>Adresse</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in items" :key="s.id">
                <td><span class="badge badge-neutral font-mono">{{ s.id }}</span></td>
                <td class="font-medium">{{ s.nom }}</td>
                <td style="color: var(--text-secondary)">{{ s.email || '—' }}</td>
                <td style="color: var(--text-secondary)">{{ s.telephone || '—' }}</td>
                <td style="color: var(--text-secondary); max-width: 200px">
                  <span class="line-clamp-1">{{ s.adresse || '—' }}</span>
                </td>
                <td class="text-right">
                  <div class="inline-flex items-center gap-2">
                    <button class="btn-ghost btn btn-sm" @click="openEdit(s)">
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                      Modifier
                    </button>
                    <button class="btn-danger btn btn-sm" @click="askDelete(s)">
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

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="modal.open" class="modal-overlay" @click.self="closeModal">
        <div class="modal-panel max-w-xl">
          <div class="flex items-start justify-between gap-4 mb-5">
            <div>
              <h2 class="text-lg font-bold">{{ modal.mode === 'create' ? 'Nouveau fournisseur' : 'Modifier le fournisseur' }}</h2>
              <p class="text-sm mt-0.5" style="color: var(--text-secondary)">Les modifications sont synchronisées avec le backend.</p>
            </div>
            <button class="btn-ghost btn btn-sm" @click="closeModal">✕</button>
          </div>

          <div v-if="saveError" class="alert alert-error mb-4">{{ saveError }}</div>

          <form class="grid grid-cols-1 sm:grid-cols-2 gap-4" @submit.prevent="submit">
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Nom <span style="color: var(--danger)">*</span></label>
              <input v-model.trim="form.nom" type="text" class="input" :class="formErrors.nom ? 'border-red-500/50' : ''" placeholder="Nom du fournisseur" />
              <p v-if="formErrors.nom" class="mt-1 text-xs" style="color: var(--danger)">{{ formErrors.nom }}</p>
            </div>
            <div>
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Email</label>
              <input v-model.trim="form.email" type="email" class="input" placeholder="contact@fournisseur.com" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Téléphone</label>
              <input v-model.trim="form.telephone" type="text" class="input" placeholder="+212 ..." />
            </div>
            <div class="sm:col-span-2">
              <label class="block text-sm font-medium mb-1.5" style="color: var(--text-secondary)">Adresse</label>
              <textarea v-model.trim="form.adresse" rows="2" class="input resize-none" placeholder="Adresse complète..." />
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
      message="Ce fournisseur sera supprimé définitivement."
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
import { listSuppliers, createSupplier, updateSupplier, deleteSupplier } from '../services/suppliers'

const loading = ref(false), error = ref(null)
const items = ref([]), page = ref(1), totalPages = ref(1), totalCount = ref(null)
const search = ref(''), activeSearch = ref('')

const modal = reactive({ open: false, mode: 'create' })
const form = reactive({ id: null, nom: '', email: '', telephone: '', adresse: '' })
const formErrors = reactive({ nom: '' })
const saving = ref(false), saveError = ref(null)
const deleteModal = reactive({ open: false, item: null, loading: false })

async function fetchData() {
  loading.value = true; error.value = null
  try {
    const params = { page: page.value, page_size: 10 }
    if (activeSearch.value) params.search = activeSearch.value
    const res = await listSuppliers(params)
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

function applySearch() { activeSearch.value = search.value; page.value = 1; fetchData() }
function clearSearch() { search.value = ''; activeSearch.value = ''; page.value = 1; fetchData() }
function onPageChange(p) { page.value = p; fetchData() }

function openCreate() {
  modal.mode = 'create'; Object.assign(form, { id: null, nom: '', email: '', telephone: '', adresse: '' })
  formErrors.nom = ''; saveError.value = null; modal.open = true
}
function openEdit(s) {
  modal.mode = 'edit'; Object.assign(form, { id: s.id, nom: s.nom, email: s.email || '', telephone: s.telephone || '', adresse: s.adresse || '' })
  formErrors.nom = ''; saveError.value = null; modal.open = true
}
function closeModal() { modal.open = false }

function validate() {
  formErrors.nom = ''
  if (!form.nom || form.nom.length < 2) { formErrors.nom = 'Nom requis (min. 2 caractères).'; return false }
  return true
}

async function submit() {
  if (!validate()) return
  saving.value = true; saveError.value = null
  try {
    const payload = { nom: form.nom, email: form.email, telephone: form.telephone, adresse: form.adresse }
    if (modal.mode === 'create') await createSupplier(payload)
    else await updateSupplier(form.id, payload)
    closeModal(); await fetchData()
  } catch (e) { saveError.value = e?.message || 'Erreur lors de l\'enregistrement.' }
  finally { saving.value = false }
}

function askDelete(s) { deleteModal.item = s; deleteModal.open = true; deleteModal.loading = false }
async function doDelete() {
  deleteModal.loading = true
  try {
    await deleteSupplier(deleteModal.item.id)
    deleteModal.open = false
    if (items.value.length === 1 && page.value > 1) page.value--
    await fetchData()
  } catch (e) { error.value = e?.message || 'Erreur lors de la suppression.'; deleteModal.open = false }
  finally { deleteModal.loading = false }
}

onMounted(fetchData)
</script>
