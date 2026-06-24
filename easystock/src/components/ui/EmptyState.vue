<template>
  <div class="flex flex-col items-center justify-center py-16 text-center gap-3">
    <div class="h-14 w-14 rounded-2xl flex items-center justify-center mb-1" style="background: rgba(255,255,255,0.04); border: 1px solid var(--border)">
      <slot name="icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--text-muted)">
          <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
        </svg>
      </slot>
    </div>
    <div>
      <p class="font-medium text-sm">{{ title }}</p>
      <p class="text-xs mt-1" style="color: var(--text-muted)">{{ subtitle }}</p>
    </div>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  title:    { type: String, default: 'Aucun résultat' },
  subtitle: { type: String, default: 'Aucun élément trouvé.' },
})
</script>
