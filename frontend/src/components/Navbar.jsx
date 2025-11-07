import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav style={{
      background: 'linear-gradient(135deg, #0ea5e9 0%, #14b8a6 100%)',
      padding: '1rem 0',
      boxShadow: '0 4px 20px rgba(14, 165, 233, 0.15)',
      borderBottom: '1px solid rgba(255,255,255,0.1)'
    }}>
      <div style={{ 
        maxWidth: '1400px', 
        margin: '0 auto', 
        padding: '0 24px', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center' 
      }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'white', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            background: 'rgba(255,255,255,0.2)',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '20px'
          }}>🏥</div>
          <h1 style={{ margin: 0, fontSize: '22px', fontWeight: '700', letterSpacing: '-0.5px' }}>
            HealthRecord Pro
          </h1>
        </Link>
        
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <NavLink to="/dashboard" label="📊 Dashboard" />
          <NavLink to="/logs" label="📝 Logs" />
          <NavLink to="/reports" label="📄 Reports" />
          <NavLink to="/insights" label="🤖 Insights" />
          <NavLink to="/profile" label="👤 Profile" />
          
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '12px', 
            marginLeft: '16px', 
            paddingLeft: '16px', 
            borderLeft: '1px solid rgba(255,255,255,0.2)' 
          }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'rgba(255,255,255,0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '16px'
            }}>👤</div>
            <span style={{ color: 'white', fontSize: '14px', fontWeight: '500' }}>
              {user?.full_name?.split(' ')[0]}
            </span>
            <button 
              onClick={handleLogout}
              style={{
                background: 'rgba(255,255,255,0.15)',
                border: '1px solid rgba(255,255,255,0.3)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600',
                fontSize: '14px',
                transition: 'all 0.2s ease',
                backdropFilter: 'blur(10px)'
              }}
              onMouseEnter={(e) => { e.currentTarget.style.background = 'rgba(255,255,255,0.25)' }}
              onMouseLeave={(e) => { e.currentTarget.style.background = 'rgba(255,255,255,0.15)' }}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

function NavLink({ to, label }) {
  const pathname = window.location.pathname
  const isActive = pathname === to
  
  return (
    <Link 
      to={to} 
      style={{ 
        color: 'white',
        textDecoration: 'none', 
        fontWeight: '500',
        fontSize: '15px',
        padding: '8px 16px',
        borderRadius: '8px',
        background: isActive ? 'rgba(255,255,255,0.2)' : 'transparent',
        transition: 'all 0.2s ease'
      }}
      onMouseEnter={(e) => {
        if (!isActive) e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
      }}
      onMouseLeave={(e) => {
        if (!isActive) e.currentTarget.style.background = 'transparent'
      }}
    >
      {label}
    </Link>
  )
}
