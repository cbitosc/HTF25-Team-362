import api from './api'

export const aiService = {
  async getInsights(days = 30) {
    const response = await api.get(`/api/ai/insights?days=${days}`)
    return response.data
  },

  async generateInsight() {
    const response = await api.post('/api/ai/generate-insight', {})
    return response.data
  },

  async getSymptomAdvice(symptom, severity = 'mild') {
    const response = await api.post('/api/ai/symptom-advice', {
      symptom,
      severity
    })
    return response.data
  },

  async chat(message, conversationHistory = null) {
    const response = await api.post('/api/ai/chat', {
      message,
      conversation_history: conversationHistory
    })
    return response.data
  },

  async analyzeSleep() {
    const response = await api.get('/api/ai/sleep-analysis')
    return response.data
  }
}
