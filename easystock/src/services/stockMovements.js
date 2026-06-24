import { api, url } from './api'

export const listStockMovements = (p = {}) => api.get(url('/api/mouvements/'), { params: p })
