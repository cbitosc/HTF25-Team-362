import api from './api'

export const logService = {
  async createLog(logData) {
    const response = await api.post('/api/logs', logData)
    return response.data
  },

  async getLogs() {
    const response = await api.get('/api/logs')
    return response.data
  },

  async getLogById(logId) {
    const response = await api.get(`/api/logs/${logId}`)
    return response.data
  },

  async updateLog(logId, logData) {
    const response = await api.put(`/api/logs/${logId}`, logData)
    return response.data
  },

  async deleteLog(logId) {
    const response = await api.delete(`/api/logs/${logId}`)
    return response.data
  }
}
