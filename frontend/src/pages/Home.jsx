import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f0fdfa, #ffffff, #f8fafc)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div style={{ textAlign: 'center', maxWidth: '800px' }}>
        <h1 style={{
          fontSize: '56px',
          fontWeight: 'bold',
          marginBottom: '16px',
          background: 'linear-gradient(135deg, #14b8a6, #0d9488)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          🏥 HealthRecord
        </h1>
        <p style={{ fontSize: '24px', color: '#64748b', marginBottom: '40px' }}>
          Your Personal Health Management System
        </p>
        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
          <Link to="/login" style={{
            background: 'linear-gradient(135deg, #14b8a6, #0d9488)',
            color: 'white',
            padding: '14px 32px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '16px'
          }}>
            Sign In
          </Link>
          <Link to="/register" style={{
            background: 'white',
            color: '#14b8a6',
            padding: '14px 32px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 'bold',
            fontSize: '16px',
            border: '2px solid #14b8a6'
          }}>
            Get Started
          </Link>
        </div>
      </div>
    </div>
  )
}
