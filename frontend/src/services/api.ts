import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add Telegram initData to requests
api.interceptors.request.use((config) => {
  const tg = window.Telegram?.WebApp
  if (tg?.initData) {
    config.headers['X-Telegram-Init-Data'] = tg.initData
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized
      console.error('Unauthorized access')
    }
    return Promise.reject(error)
  }
)

// User API
export const userAPI = {
  getProfile: () => api.get('/api/user/profile/'),
  updateProfile: (data: any) => api.put('/api/user/profile/', data),
  getUser: (userId: number) => api.get(`/api/user/${userId}/`),
  getUserWishes: (userId: number) => api.get(`/api/user/${userId}/wishes/`),
}

// Wishes API
export const wishesAPI = {
  getWishes: (params?: any) => api.get('/api/wishes/', { params }),
  getWish: (id: number) => api.get(`/api/wishes/${id}/`),
  createWish: (data: any) => api.post('/api/wishes/', data),
  updateWish: (id: number, data: any) => api.put(`/api/wishes/${id}/`, data),
  deleteWish: (id: number) => api.delete(`/api/wishes/${id}/`),
  completeWish: (id: number) => api.patch(`/api/wishes/${id}/complete/`),
}

// Groups API
export const groupsAPI = {
  getGroups: () => api.get('/api/groups/'),
  getGroup: (id: number) => api.get(`/api/groups/${id}/`),
  createGroup: (data: any) => api.post('/api/groups/', data),
  updateGroup: (id: number, data: any) => api.put(`/api/groups/${id}/`, data),
  joinGroup: (id: number, inviteCode: string) =>
    api.post(`/api/groups/${id}/join/`, { invite_code: inviteCode }),
  getMembers: (id: number) => api.get(`/api/groups/${id}/members/`),
  getGroupWishes: (id: number) => api.get(`/api/groups/${id}/wishes/`),
}

export default api
