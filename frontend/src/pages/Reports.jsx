import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import LoadingSpinner from '../components/LoadingSpinner'
import UploadReportForm from '../components/UploadReportForm'
import api from '../services/api'

export default function Reports() {
  const { user, token } = useAuth()
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [generatingReport, setGeneratingReport] = useState(false)

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      const response = await api.get('/api/reports')
      setReports(response.data)
    } catch (error) {
      console.error('Error fetching reports:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (reportId) => {
    if (!window.confirm('Are you sure you want to delete this report?')) return
    
    try {
      await api.delete(`/api/reports/${reportId}`)
      fetchReports()
    } catch (error) {
      console.error('Error deleting report:', error)
      alert('Failed to delete report')
    }
  }

  const generateHealthReport = async () => {
    setGeneratingReport(true)
    try {
      const response = await api.get('/api/reports/export-summary', {
        responseType: 'blob' // Important for downloading files
      })
      
      // Create blob and download
      const blob = new Blob([response.data], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `health_report_${user.full_name.replace(' ', '_')}_${new Date().toISOString().split('T')[0]}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error generating report:', error)
      alert('Failed to generate health report')
    } finally {
      setGeneratingReport(false)
    }
  }

  if (!user) return <LoadingSpinner />

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
          <h2 style={{ fontSize: '28px', fontWeight: 'bold' }}>Medical Reports</h2>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button 
              onClick={generateHealthReport}
              disabled={generatingReport}
              style={{
                background: generatingReport 
                  ? '#94a3b8' 
                  : 'linear-gradient(135deg, #3b82f6, #2563eb)',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '8px',
                fontWeight: 'bold',
                cursor: generatingReport ? 'not-allowed' : 'pointer',
                opacity: generatingReport ? 0.6 : 1
              }}
            >
              {generatingReport ? '⏳ Generating...' : '📋 Generate Health Report'}
            </button>
            <button 
              onClick={() => setShowForm(!showForm)}
              style={{
                background: 'linear-gradient(135deg, #14b8a6, #0d9488)',
                color: 'white',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '8px',
                fontWeight: 'bold',
                cursor: 'pointer'
              }}
            >
              {showForm ? '❌ Cancel' : '📄 Upload Report'}
            </button>
          </div>
        </div>

        {/* Info Banner for Generated Reports */}
        <div style={{
          background: 'linear-gradient(135deg, #dbeafe, #bfdbfe)',
          border: '2px solid #3b82f6',
          borderRadius: '12px',
          padding: '20px',
          marginBottom: '24px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
            <span style={{ fontSize: '24px' }}>📋</span>
            <h3 style={{ margin: 0, color: '#1e40af', fontSize: '18px' }}>Generate Health Report</h3>
          </div>
          <p style={{ color: '#1e3a8a', margin: 0, fontSize: '14px' }}>
            Click "Generate Health Report" to create a comprehensive PDF document containing your health logs, vital signs, 
            symptoms, and medical reports. This professional document can be shared with your doctor for appointments.
          </p>
        </div>

        {showForm && <UploadReportForm onSuccess={() => { setShowForm(false); fetchReports(); }} />}

        {loading ? (
          <LoadingSpinner />
        ) : reports.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '60px 20px', color: '#64748b' }}>
            <div style={{ fontSize: '64px', marginBottom: '16px' }}>📄</div>
            <p>No reports yet. Upload your first report!</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '20px' }}>
            {reports.map((report) => (
              <div key={report.id} style={{
                background: 'white',
                padding: '24px',
                borderRadius: '16px',
                boxShadow: '0 4px 16px rgba(0,0,0,0.06)'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '12px' }}>
                  <h3 style={{ fontSize: '18px', fontWeight: 'bold', margin: 0 }}>{report.title}</h3>
                  <span style={{ color: '#64748b', fontSize: '14px' }}>
                    {new Date(report.report_date).toLocaleDateString()}
                  </span>
                </div>
                <div style={{ marginBottom: '8px', fontSize: '12px', color: '#64748b', textTransform: 'capitalize' }}>
                  {report.report_type?.replace('_', ' ')}
                </div>
                {report.description && <p style={{ color: '#64748b', marginBottom: '12px' }}>{report.description}</p>}
                <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                  {report.file_name && (
                    <a 
                      href={`http://127.0.0.1:8000/static/uploads/${report.file_name}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: '#14b8a6',
                        textDecoration: 'none',
                        fontWeight: '500'
                      }}
                    >
                      📎 View File
                    </a>
                  )}
                  <button
                    onClick={() => handleDelete(report.id)}
                    style={{
                      background: '#fee2e2',
                      color: '#dc2626',
                      border: 'none',
                      padding: '6px 12px',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '14px',
                      fontWeight: '500'
                    }}
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  )
}
