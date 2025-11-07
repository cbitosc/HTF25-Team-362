import api from './api'

export const authService = {
  async register(userData) {
    const response = await api.post('/api/auth/register', userData)
    return response.data
  },

  async login(email, password) {
    const response = await api.post('/api/auth/login', { email, password })
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/api/auth/me')
    return response.data
  },

  async updateProfile(userData) {
    const response = await api.put('/api/auth/me', userData)
    return response.data
  },

  async verifyToken() {
    const response = await api.get('/api/auth/verify-token')
    return response.data
  },

  async logout() {
    await api.post('/api/auth/logout')
  }
}
