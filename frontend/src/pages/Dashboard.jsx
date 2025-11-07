import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import LoadingSpinner from '../components/LoadingSpinner'
import api from '../services/api'

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState({ logs: 0, reports: 0 })
  const navigate = useNavigate()

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const [logsRes, reportsRes] = await Promise.all([
        api.get('/api/logs'),
        api.get('/api/reports')
      ])
      setStats({
        logs: logsRes.data.length || 0,
        reports: reportsRes.data.length || 0
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  if (!user) return <LoadingSpinner />

  return (
    <>
      <Navbar />
      <div style={{ 
        maxWidth: '1400px', 
        margin: '0 auto', 
        padding: '48px 24px',
        minHeight: 'calc(100vh - 80px)'
      }}>
        {/* Welcome Section */}
        <div style={{ 
          marginBottom: '48px',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          borderRadius: '24px',
          padding: '48px',
          color: 'white',
          boxShadow: '0 20px 60px rgba(102, 126, 234, 0.3)'
        }}>
          <div style={{ 
            fontSize: '16px', 
            opacity: 1, 
            marginBottom: '8px',
            color: 'white',
            fontWeight: '500',
            letterSpacing: '0.5px'
          }}>
            Good to see you again!
          </div>
          <h1 style={{ 
            fontSize: '40px', 
            fontWeight: '800', 
            marginBottom: '16px',
            letterSpacing: '-1px',
            lineHeight: '1.2'
          }}>
            Welcome back, {user.full_name?.split(' ')[0]}! 👋
          </h1>
          <p style={{ 
            fontSize: '18px', 
            opacity: 1, 
            maxWidth: '600px',
            color: 'white',
            textShadow: '0 2px 8px rgba(0,0,0,0.2)',
            fontWeight: '500',
            letterSpacing: '0.3px'
          }}>
            Manage your health records, track your progress, and gain AI-powered insights to stay on top of your wellness.
          </p>
        </div>

        {/* Stats Cards */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
          gap: '24px',
          marginBottom: '48px'
        }}>
          {[
            { title: 'Health Logs', count: stats.logs, emoji: '📊', link: '/logs', color: '#14b8a6', gradient: 'linear-gradient(135deg, #14b8a6, #0d9488)' },
            { title: 'Medical Reports', count: stats.reports, emoji: '📄', link: '/reports', color: '#3b82f6', gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)' },
            { title: 'AI Insights', count: 'New', emoji: '🤖', link: '/insights', color: '#8b5cf6', gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)' },
            { title: 'Profile Settings', emoji: '⚙️', link: '/profile', color: '#f59e0b', gradient: 'linear-gradient(135deg, #f59e0b, #d97706)' }
          ].map((card, i) => (
            <div 
              key={i} 
              style={{
                background: 'white',
                padding: '32px',
                borderRadius: '20px',
                cursor: 'pointer',
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
                border: '1px solid rgba(226, 232, 240, 0.8)',
                position: 'relative',
                overflow: 'hidden'
              }} 
              onClick={() => navigate(card.link)}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px)'
                e.currentTarget.style.boxShadow = '0 12px 40px rgba(0,0,0,0.12)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)'
                e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)'
              }}
            >
              <div style={{
                width: '56px',
                height: '56px',
                background: card.gradient,
                borderRadius: '16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '28px',
                marginBottom: '20px'
              }}>
                {card.emoji}
              </div>
              <h3 style={{ fontSize: '20px', fontWeight: '700', marginBottom: '12px', color: '#1e293b' }}>
                {card.title}
              </h3>
              {card.count && (
                <div style={{ 
                  fontSize: card.count === 'New' ? '16px' : '32px', 
                  fontWeight: '800', 
                  background: card.gradient,
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}>
                  {card.count}
                </div>
              )}
              <div style={{
                marginTop: '20px',
                fontSize: '14px',
                color: '#64748b',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}>
                {card.count === 'New' ? (
                  <>
                    <span style={{ fontSize: '18px' }}>→</span> Generate insights
                  </>
                ) : (
                  <>
                    <span style={{ fontSize: '18px' }}>→</span> View details
                  </>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Quick Actions */}
        <div style={{
          background: 'white',
          borderRadius: '20px',
          padding: '32px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
        }}>
          <h2 style={{ fontSize: '24px', fontWeight: '700', marginBottom: '24px', color: '#1e293b' }}>
            Quick Actions
          </h2>
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            <button onClick={() => navigate('/logs')} style={{
              padding: '16px 32px',
              background: 'linear-gradient(135deg, #14b8a6, #0d9488)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontWeight: '600',
              fontSize: '16px',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(20, 184, 166, 0.3)',
              transition: 'all 0.2s'
            }}>
              + Add Health Log
            </button>
            <button onClick={() => navigate('/reports')} style={{
              padding: '16px 32px',
              background: 'white',
              color: '#3b82f6',
              border: '2px solid #3b82f6',
              borderRadius: '12px',
              fontWeight: '600',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}>
              📤 Upload Report
            </button>
            <button onClick={() => navigate('/insights')} style={{
              padding: '16px 32px',
              background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontWeight: '600',
              fontSize: '16px',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(139, 92, 246, 0.3)',
              transition: 'all 0.2s'
            }}>
              🤖 Get AI Insights
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
