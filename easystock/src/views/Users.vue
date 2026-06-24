<template>
  <div class="space-y-6 animate-fade-in">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Utilisateurs</h1>
      <p class="text-sm mt-1" style="color: var(--text-secondary)">Gestion des comptes utilisateurs Django.</p>
    </div>
    <div class="card p-10 text-center">
      <div class="h-14 w-14 rounded-2xl flex items-center justify-center mx-auto mb-4" style="background: var(--accent-dim); border: 1px solid var(--accent-glow)">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
        </svg>
      </div>
      <h2 class="font-semibold text-lg mb-2">Gestion via Django Admin</h2>
      <p class="text-sm mb-5" style="color: var(--text-secondary)">La gestion des utilisateurs est disponible dans l'interface d'administration Django.</p>
      <a href="http://127.0.0.1:8000/admin/auth/user/" target="_blank" rel="noopener" class="btn-primary btn inline-flex">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        Ouvrir Django Admin
      </a>
    </div>
  </div>
</template>
