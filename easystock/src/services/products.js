import { api, url } from './api'

export const listProducts    = (p = {})      => api.get(url('/api/produits/'), { params: p })
export const getProduct      = (id)           => api.get(url(`/api/produits/${id}/`))
export const createProduct   = (payload)      => api.post(url('/api/produits/'), payload)
export const updateProduct   = (id, payload)  => api.put(url(`/api/produits/${id}/`), payload)
export const deleteProduct   = (id)           => api.delete(url(`/api/produits/${id}/`))
export const getLowStock     = ()             => api.get(url('/api/produits/stock_faible/'))
export const getOutOfStock   = ()             => api.get(url('/api/produits/rupture_stock/'))
export const getProductHistory = (id)         => api.get(url(`/api/produits/${id}/historique/`))
