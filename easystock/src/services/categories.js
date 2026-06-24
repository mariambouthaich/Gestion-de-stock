import { api, url } from './api'

export const listCategories   = (p = {})      => api.get(url('/api/categories/'), { params: p })
export const getCategory      = (id)           => api.get(url(`/api/categories/${id}/`))
export const createCategory   = (payload)      => api.post(url('/api/categories/'), payload)
export const updateCategory   = (id, payload)  => api.put(url(`/api/categories/${id}/`), payload)
export const deleteCategory   = (id)           => api.delete(url(`/api/categories/${id}/`))
export const getCategoryProducts = (id)        => api.get(url(`/api/categories/${id}/produits/`))
