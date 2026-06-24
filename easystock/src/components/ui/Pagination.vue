<template>
  <div v-if="totalPages > 1" class="flex items-center justify-between gap-3 pt-4 mt-1 border-t" style="border-color: var(--border)">
    <span class="text-xs" style="color: var(--text-muted)">
      Page {{ page }} / {{ totalPages }}
      <span v-if="totalCount"> — {{ totalCount }} résultats</span>
    </span>
    <div class="flex items-center gap-1">
      <button class="btn-ghost btn btn-sm" :disabled="page <= 1 || loading" @click="$emit('change', page - 1)">
        ← Préc
      </button>
      <button class="btn-ghost btn btn-sm" :disabled="page >= totalPages || loading" @click="$emit('change', page + 1)">
        Suiv →
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  page:       { type: Number, required: true },
  totalPages: { type: Number, required: true },
  totalCount: { type: Number, default: null },
  loading:    { type: Boolean, default: false },
})
defineEmits(['change'])
</script>
