<template>
  <Teleport to="body">
    <div v-if="open" class="modal-overlay animate-fade-in" @click.self="$emit('cancel')">
      <div class="modal-panel max-w-sm">
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0 h-10 w-10 rounded-xl flex items-center justify-center" style="background: var(--danger-dim); border: 1px solid rgba(248,113,113,0.2)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f87171" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 6h18M19 6l-1 14H6L5 6M10 11v6M14 11v6M9 6V4h6v2"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-semibold text-base">{{ title }}</h3>
            <p class="mt-1 text-sm" style="color: var(--text-secondary)">{{ message }}</p>
          </div>
        </div>
        <div class="mt-5 flex justify-end gap-2">
          <button class="btn-ghost btn" @click="$emit('cancel')">Annuler</button>
          <button class="btn-danger btn" :disabled="loading" @click="$emit('confirm')">
            <svg v-if="loading" class="animate-spin" width="14" height="14" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
            </svg>
            {{ confirmLabel }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  open:         { type: Boolean, default: false },
  title:        { type: String,  default: 'Confirmer la suppression' },
  message:      { type: String,  default: 'Cette action est irréversible.' },
  confirmLabel: { type: String,  default: 'Supprimer' },
  loading:      { type: Boolean, default: false },
})
defineEmits(['confirm', 'cancel'])
</script>
