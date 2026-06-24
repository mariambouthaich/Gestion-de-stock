import { api, url } from './api'
export const getDashboardStats = () => api.get(url('/api/stats/'))
