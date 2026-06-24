<template>
  <div :class="['flex items-center justify-center', fullPage ? 'min-h-[40vh]' : 'py-10']">
    <div class="flex flex-col items-center gap-3">
      <svg class="animate-spin" :width="size" :height="size" viewBox="0 0 24 24" fill="none">
        <circle class="opacity-20" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" />
        <path class="opacity-80" fill="currentColor" d="M4 12a8 8 0 018-8v3a5 5 0 00-5 5H4z" />
      </svg>
      <span v-if="label" class="text-sm" style="color: var(--text-muted)">{{ label }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  size:     { type: Number, default: 28 },
  label:    { type: String, default: '' },
  fullPage: { type: Boolean, default: false },
})
</script>
