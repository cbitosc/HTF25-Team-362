import api from './api'

export const reportService = {
  async uploadReport(formData) {
    const response = await api.post('/api/reports/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  async getReports() {
    const response = await api.get('/api/reports')
    return response.data
  },

  async getReportById(reportId) {
    const response = await api.get(`/api/reports/${reportId}`)
    return response.data
  },

  async updateReport(reportId, reportData) {
    const response = await api.put(`/api/reports/${reportId}`, reportData)
    return response.data
  },

  async deleteReport(reportId) {
    const response = await api.delete(`/api/reports/${reportId}`)
    return response.data
  }
}
