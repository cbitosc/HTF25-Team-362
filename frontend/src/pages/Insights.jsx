import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import LoadingSpinner from '../components/LoadingSpinner'
import api from '../services/api'

export default function Insights() {
  const { user } = useAuth()
  const [logs, setLogs] = useState([])
  const [selectedLogs, setSelectedLogs] = useState([])
  const [insight, setInsight] = useState(null)
  const [savedInsights, setSavedInsights] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [isFromDatabase, setIsFromDatabase] = useState(false)

  useEffect(() => {
    fetchLogs()
    fetchSavedInsights()
  }, [])

  const fetchLogs = async () => {
    try {
      const response = await api.get('/api/logs')
      setLogs(response.data)
    } catch (error) {
      console.error('Error fetching logs:', error)
    }
  }

  const fetchSavedInsights = async () => {
    try {
      const response = await api.get('/api/ai/saved-insights')
      setSavedInsights(response.data.insights || [])
    } catch (error) {
      console.error('Error fetching saved insights:', error)
    }
  }

  const handleToggleLog = (logId) => {
    if (selectedLogs.includes(logId)) {
      setSelectedLogs(selectedLogs.filter(id => id !== logId))
    } else {
      setSelectedLogs([...selectedLogs, logId])
    }
  }

  const renderValue = (value) => {
    if (typeof value === 'object' && value !== null) {
      if (Array.isArray(value)) {
        return value.join(', ')
      }
      return Object.entries(value).map(([k, v]) => `${k}: ${v}`).join(', ')
    }
    return value
  }

  const parseInsights = (insightsText) => {
    if (!insightsText) return null
    
    try {
      // Try to extract JSON from code block
      const jsonMatch = insightsText.match(/```json\s*([\s\S]*?)\s*```/) || insightsText.match(/```\s*([\s\S]*?)\s*```/)
      if (jsonMatch && jsonMatch[1]) {
        return JSON.parse(jsonMatch[1])
      }
      
      // If it's already parsed JSON object
      if (typeof insightsText === 'object') {
        return insightsText
      }
      
      // Try parsing as JSON string
      return JSON.parse(insightsText)
    } catch (e) {
      // If parsing fails, return as text
      return { rawText: insightsText }
    }
  }

  const generateInsight = async () => {
    if (selectedLogs.length === 0) {
      setError('Please select at least one log to analyze')
      return
    }

    setLoading(true)
    setError('')
    setInsight(null)

    try {
      // Use the main insights endpoint
      const response = await api.get('/api/ai/insights?days=365')
      
      // Parse insights
      const parsedInsights = parseInsights(response.data.insights)
      
      // Enhance with selected logs info
      const enhancedData = {
        ...response.data,
        insights: parsedInsights,
        selected_logs_count: selectedLogs.length,
        total_logs_in_system: logs.length,
        patient_name: user?.full_name || 'Patient'
      }
      
      setInsight(enhancedData)
      setIsFromDatabase(false) // Mark as newly generated from AI
      
      // Auto-save the insight
      await saveInsightToDB(enhancedData)
    } catch (error) {
      setError('Failed to generate insight: ' + (error.response?.data?.detail || 'Please try again.'))
      console.error('Error generating insight:', error)
    } finally {
      setLoading(false)
    }
  }

  const saveInsightToDB = async (insightData) => {
    try {
      await api.post('/api/ai/save-insight', {
        patient_name: insightData.patient_name,
        log_ids: selectedLogs,
        logs_analyzed: insightData.logs_analyzed,
        insights_raw: insightData.insights_raw || JSON.stringify(insightData.insights),
        insights: insightData.insights,
        data_points_analyzed: insightData.data_points_analyzed
      })
      
      // Refresh saved insights
      fetchSavedInsights()
    } catch (error) {
      console.error('Error saving insight:', error)
    }
  }

  const loadSavedInsight = (savedInsight) => {
    setInsight({
      patient_name: savedInsight.patient_name,
      logs_analyzed: savedInsight.logs_analyzed_count,
      data_points_analyzed: savedInsight.data_points_analyzed,
      insights: {
        trends: savedInsight.trends,
        correlations: savedInsight.correlations,
        recommendations: savedInsight.recommendations || [],
        alerts: savedInsight.alerts
      }
    })
    setIsFromDatabase(true) // Mark as loaded from database
  }

  const reAnalyze = async () => {
    // Re-run analysis with same selection
    await generateInsight()
  }

  const deleteInsight = async (insightId) => {
    if (!window.confirm('Are you sure you want to delete this saved insight?')) return
    
    try {
      await api.delete(`/api/ai/saved-insights/${insightId}`)
      // Reload insights list
      fetchSavedInsights()
      // Clear current insight if it was the deleted one
      if (insight && insight.id === insightId) {
        setInsight(null)
        setIsFromDatabase(false)
      }
    } catch (error) {
      console.error('Error deleting insight:', error)
      alert('Failed to delete insight')
    }
  }

  const printInsights = () => {
    window.print()
  }

  const handlePrint = () => {
    window.print()
  }

  if (!user) return <LoadingSpinner />

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px' }}>
        <h2 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '32px' }}>AI Health Insights</h2>

        {/* Saved Insights */}
        {savedInsights.length > 0 && (
          <div style={{
            background: 'white',
            padding: '24px',
            borderRadius: '16px',
            boxShadow: '0 4px 16px rgba(0,0,0,0.06)',
            marginBottom: '24px'
          }}>
            <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>📋 Previously Saved Insights</h3>
            <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              {savedInsights.map(ins => (
                <div key={ins.id} style={{
                  background: '#f0fdfa',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  border: '1px solid #14b8a6'
                }}>
                  <div style={{ fontWeight: '600', marginBottom: '4px' }}>{ins.patient_name || 'Patient'}</div>
                  <div style={{ fontSize: '12px', color: '#64748b' }}>
                    {new Date(ins.analysis_date).toLocaleDateString()} • {ins.logs_analyzed_count} logs
                  </div>
                  <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                    <button
                      onClick={() => loadSavedInsight(ins)}
                      style={{
                        background: '#14b8a6',
                        color: 'white',
                        border: 'none',
                        padding: '6px 12px',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontSize: '12px'
                      }}
                    >
                      View
                    </button>
                    <button
                      onClick={() => deleteInsight(ins.id)}
                      style={{
                        background: '#fee2e2',
                        color: '#dc2626',
                        border: 'none',
                        padding: '6px 12px',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        fontSize: '12px'
                      }}
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Log Selection */}
        <div style={{
          background: 'white',
          padding: '32px',
          borderRadius: '16px',
          boxShadow: '0 4px 16px rgba(0,0,0,0.06)',
          marginBottom: '24px'
        }}>
          <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>Select Logs to Analyze</h3>
          
          {logs.length === 0 ? (
            <p style={{ color: '#64748b' }}>No logs available</p>
          ) : (
            <div style={{ maxHeight: '300px', overflowY: 'auto', marginBottom: '16px' }}>
              {logs.map(log => (
                <label key={log.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  padding: '12px',
                  marginBottom: '8px',
                  background: selectedLogs.includes(log.id) ? '#f0fdfa' : '#f8fafc',
                  border: `2px solid ${selectedLogs.includes(log.id) ? '#14b8a6' : '#e2e8f0'}`,
                  borderRadius: '8px',
                  cursor: 'pointer'
                }}>
                  <input
                    type="checkbox"
                    checked={selectedLogs.includes(log.id)}
                    onChange={() => handleToggleLog(log.id)}
                    style={{ marginRight: '12px', cursor: 'pointer' }}
                  />
                  <div>
                    <div style={{ fontWeight: '600', color: selectedLogs.includes(log.id) ? '#0d9488' : '#1e293b' }}>
                      Log - {log.patient_name || 'Patient'} ({log.mood || 'N/A'})
                    </div>
                    <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>
                      {log.log_date ? new Date(log.log_date).toLocaleDateString() : 'No date'}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          )}

          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              onClick={generateInsight}
              disabled={loading || selectedLogs.length === 0}
              style={{
                background: loading || selectedLogs.length === 0 ? '#94a3b8' : 'linear-gradient(135deg, #14b8a6, #0d9488)',
                color: 'white',
                border: 'none',
                padding: '14px 32px',
                borderRadius: '8px',
                fontWeight: 'bold',
                cursor: loading || selectedLogs.length === 0 ? 'not-allowed' : 'pointer',
                fontSize: '16px'
              }}
            >
              {loading ? '⏳ Generating...' : `🤖 Analyze ${selectedLogs.length} Log${selectedLogs.length !== 1 ? 's' : ''}`}
            </button>
            
            {selectedLogs.length > 0 && (
              <button
                onClick={() => setSelectedLogs([])}
                style={{
                  background: '#fee2e2',
                  color: '#dc2626',
                  border: 'none',
                  padding: '14px 24px',
                  borderRadius: '8px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                Clear Selection
              </button>
            )}
          </div>
        </div>

        {error && (
          <div style={{
            padding: '12px',
            background: '#fee2e2',
            color: '#dc2626',
            borderRadius: '8px',
            marginBottom: '24px'
          }}>
            {error}
          </div>
        )}

        {/* AI Insights Display */}
        {insight && (
          <div id="insight-content" style={{
            background: 'white',
            padding: '32px',
            borderRadius: '16px',
            boxShadow: '0 4px 16px rgba(0,0,0,0.06)',
            marginBottom: '24px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
              <div>
                <h3 style={{ fontSize: '24px', fontWeight: 'bold', color: '#0f766e', marginBottom: '8px' }}>
                  📊 AI Health Analysis Report
                </h3>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  {isFromDatabase ? (
                    <span style={{
                      background: '#dbeafe',
                      color: '#1e40af',
                      padding: '4px 12px',
                      borderRadius: '16px',
                      fontSize: '12px',
                      fontWeight: '600'
                    }}>
                      📦 Loaded from Database
                    </span>
                  ) : (
                    <span style={{
                      background: '#d1fae5',
                      color: '#065f46',
                      padding: '4px 12px',
                      borderRadius: '16px',
                      fontSize: '12px',
                      fontWeight: '600'
                    }}>
                      🤖 Fresh AI Analysis
                    </span>
                  )}
                  <span style={{
                    background: '#fef3c7',
                    color: '#92400e',
                    padding: '4px 12px',
                    borderRadius: '16px',
                    fontSize: '12px',
                    fontWeight: '600'
                  }}>
                    📚 Data History Preserved
                  </span>
                </div>
              </div>
              <div style={{ display: 'flex', gap: '12px' }}>
                {isFromDatabase && (
                  <button
                    onClick={reAnalyze}
                    style={{
                      background: 'linear-gradient(135deg, #14b8a6, #0d9488)',
                      color: 'white',
                      border: 'none',
                      padding: '10px 20px',
                      borderRadius: '8px',
                      fontWeight: 'bold',
                      cursor: 'pointer'
                    }}
                  >
                    🔄 Re-analyze with AI
                  </button>
                )}
                <button
                  onClick={handlePrint}
                  style={{
                    background: 'linear-gradient(135deg, #06b6d4, #0891b2)',
                    color: 'white',
                    border: 'none',
                    padding: '10px 20px',
                    borderRadius: '8px',
                    fontWeight: 'bold',
                    cursor: 'pointer'
                  }}
                >
                  🖨️ Print / Download
                </button>
              </div>
            </div>

            <div style={{ lineHeight: '1.8', color: '#334155' }}>
              <div style={{ marginBottom: '20px' }}>
                <strong style={{ color: '#0f766e', fontSize: '16px' }}>Patient Name:</strong>{' '}
                {insight.patient_name || 'N/A'}
              </div>

              <div style={{ marginBottom: '20px' }}>
                <strong style={{ color: '#0f766e', fontSize: '16px' }}>Logs Analyzed:</strong>{' '}
                {insight.logs_analyzed || 0}
              </div>

              {/* Display parsed insights if available */}
              {insight.insights && typeof insight.insights === 'object' && !insight.insights.rawText ? (
                <div>
                  {/* Trends */}
                  {insight.insights.trends && (
                    <div style={{ marginBottom: '24px' }}>
                      <h4 style={{ color: '#0d9488', fontSize: '18px', marginBottom: '12px', fontWeight: 'bold' }}>
                        📈 Health Trends
                      </h4>
                      <div style={{ background: '#f0fdfa', padding: '16px', borderRadius: '8px' }}>
                        {Object.entries(insight.insights.trends).map(([key, value]) => (
                          <div key={key} style={{ marginBottom: '8px' }}>
                            <strong style={{ color: '#0d9488' }}>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong> {renderValue(value)}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Correlations */}
                  {insight.insights.correlations && (
                    <div style={{ marginBottom: '24px' }}>
                      <h4 style={{ color: '#0d9488', fontSize: '18px', marginBottom: '12px', fontWeight: 'bold' }}>
                        🔗 Correlations
                      </h4>
                      <div style={{ background: '#fef3c7', padding: '16px', borderRadius: '8px' }}>
                        {Object.entries(insight.insights.correlations).map(([key, value]) => (
                          <div key={key} style={{ marginBottom: '8px' }}>
                            <strong style={{ color: '#f59e0b' }}>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong> {renderValue(value)}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Recommendations */}
                  {insight.insights.recommendations && insight.insights.recommendations.length > 0 && (
                    <div style={{ marginBottom: '24px' }}>
                      <h4 style={{ color: '#0d9488', fontSize: '18px', marginBottom: '12px', fontWeight: 'bold' }}>
                        💡 Recommendations
                      </h4>
                      <div style={{ background: '#dbeafe', padding: '16px', borderRadius: '8px' }}>
                        <ul style={{ margin: 0, paddingLeft: '20px' }}>
                          {insight.insights.recommendations.map((rec, index) => (
                            <li key={index} style={{ marginBottom: '8px' }}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Alerts */}
                  {insight.insights.alerts && (
                    <div style={{ marginBottom: '24px' }}>
                      <h4 style={{ color: '#dc2626', fontSize: '18px', marginBottom: '12px', fontWeight: 'bold' }}>
                        ⚠️ Important Alerts
                      </h4>
                      <div style={{ background: '#fee2e2', padding: '16px', borderRadius: '8px' }}>
                        {Object.entries(insight.insights.alerts).map(([key, value]) => (
                          <div key={key} style={{ marginBottom: '8px' }}>
                            <strong style={{ color: '#dc2626' }}>{key.charAt(0).toUpperCase() + key.slice(1)}:</strong> {renderValue(value)}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div style={{
                  background: '#f0fdfa',
                  padding: '20px',
                  borderRadius: '12px',
                  borderLeft: '4px solid #14b8a6',
                  whiteSpace: 'pre-wrap',
                  fontSize: '15px'
                }}>
                  <h4 style={{ color: '#0d9488', marginBottom: '12px' }}>AI Insights:</h4>
                  {insight.insights?.rawText || insight.insights || 'No insights available'}
                </div>
              )}

              {insight.data_points_analyzed && (
                <div style={{ marginTop: '20px', fontSize: '14px', color: '#64748b' }}>
                  Data points analyzed: {insight.data_points_analyzed}
                </div>
              )}
            </div>

            {/* Database History Info */}
            {isFromDatabase && savedInsights.length > 1 && (
              <div style={{
                marginTop: '24px',
                padding: '16px',
                background: '#eff6ff',
                borderRadius: '8px',
                borderLeft: '4px solid #3b82f6'
              }}>
                <strong style={{ color: '#1e40af' }}>📚 Analysis History:</strong>
                <div style={{ marginTop: '8px', fontSize: '14px', color: '#1e3a8a' }}>
                  You have {savedInsights.length} saved analysis in the database.
                  This insight was generated on {new Date(savedInsights[0]?.analysis_date || Date.now()).toLocaleString()}.
                </div>
              </div>
            )}

            {!isFromDatabase && (
              <div style={{
                marginTop: '24px',
                padding: '16px',
                background: '#f0fdf4',
                borderRadius: '8px',
                borderLeft: '4px solid #10b981'
              }}>
                <strong style={{ color: '#065f46' }}>💾 Saving to History:</strong>
                <div style={{ marginTop: '8px', fontSize: '14px', color: '#047857' }}>
                  This analysis is being saved to your database for future reference.
                  You can retrieve it later from your saved insights.
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Print Styles */}
      <style>{`
        @media print {
          body * {
            visibility: hidden;
          }
          #insight-content, #insight-content * {
            visibility: visible;
          }
          #insight-content {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
          }
        }
      `}</style>
    </>
  )
}
