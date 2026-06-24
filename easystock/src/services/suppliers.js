import { api, url } from './api'

export const listSuppliers   = (p = {})      => api.get(url('/api/fournisseurs/'), { params: p })
export const getSupplier     = (id)           => api.get(url(`/api/fournisseurs/${id}/`))
export const createSupplier  = (payload)      => api.post(url('/api/fournisseurs/'), payload)
export const updateSupplier  = (id, payload)  => api.put(url(`/api/fournisseurs/${id}/`), payload)
export const deleteSupplier  = (id)           => api.delete(url(`/api/fournisseurs/${id}/`))
