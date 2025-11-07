import { useState } from 'react'
import { logService } from '../services/logService'

export default function HealthLogForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    // Patient and Doctor Info
    patient_name: '',
    doctor_name: '',
    
    // Vitals
    temperature: '37.0',
    blood_pressure_systolic: '120',
    blood_pressure_diastolic: '80',
    
    // Symptoms (booleans)
    has_fever: false,
    has_cough: false,
    has_headache: false,
    has_fatigue: false,
    has_body_pain: false,
    has_nausea: false,
    
    // Mood and Pain
    mood: 'okay',  // Enum: 'excellent', 'good', 'okay', 'low'
    pain_level: 'none',  // Enum: 'none', 'mild', 'moderate', 'severe', 'critical'
    
    // Lifestyle
    sleep_hours: '7.5',
    sleep_quality: 5,
    stress_level: 5,
    anxiety_level: 5,
    
    // Notes
    notes: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // Prepare data for backend with proper types and all required fields
      const logData = {
        patient_name: formData.patient_name || null,
        doctor_name: formData.doctor_name || null,
        temperature: formData.temperature ? parseFloat(formData.temperature) : null,
        blood_pressure_systolic: formData.blood_pressure_systolic ? parseInt(formData.blood_pressure_systolic) : null,
        blood_pressure_diastolic: formData.blood_pressure_diastolic ? parseInt(formData.blood_pressure_diastolic) : null,
        has_fever: formData.has_fever,
        has_cough: formData.has_cough,
        has_headache: formData.has_headache,
        has_fatigue: formData.has_fatigue,
        has_body_pain: formData.has_body_pain,
        has_nausea: formData.has_nausea,
        mood: formData.mood,
        pain_level: formData.pain_level,
        sleep_hours: formData.sleep_hours ? parseFloat(formData.sleep_hours) : null,
        sleep_quality: parseInt(formData.sleep_quality),
        stress_level: parseInt(formData.stress_level),
        anxiety_level: parseInt(formData.anxiety_level),
        notes: formData.notes || null
      }
      
      console.log('Sending log data:', logData)
      
      await logService.createLog(logData)
      onSuccess && onSuccess()
      
      // Reset form
      setFormData({
        patient_name: '',
        doctor_name: '',
        temperature: '37.0',
        blood_pressure_systolic: '120',
        blood_pressure_diastolic: '80',
        has_fever: false,
        has_cough: false,
        has_headache: false,
        has_fatigue: false,
        has_body_pain: false,
        has_nausea: false,
        mood: 'okay',
        pain_level: 'none',
        sleep_hours: '7.5',
        sleep_quality: 5,
        stress_level: 5,
        anxiety_level: 5,
        notes: ''
      })
    } catch (err) {
      setError('Failed to save log: ' + (err.response?.data?.detail || err.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      background: 'white',
      padding: '24px',
      borderRadius: '16px',
      boxShadow: '0 4px 16px rgba(0,0,0,0.06)',
      border: '1px solid #e2e8f0'
    }}>
      <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '16px' }}>
        📊 Daily Health Log
      </h3>

      {error && (
        <div style={{
          padding: '12px',
          background: '#fee2e2',
          color: '#dc2626',
          borderRadius: '8px',
          marginBottom: '16px',
          fontSize: '14px'
        }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Patient and Doctor Info */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
              Patient Name
            </label>
            <input
              type="text"
              value={formData.patient_name}
              onChange={(e) => setFormData({...formData, patient_name: e.target.value})}
              placeholder="Patient name"
              style={{
                width: '100%',
                padding: '12px',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '14px'
              }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
              Doctor Name
            </label>
            <input
              type="text"
              value={formData.doctor_name}
              onChange={(e) => setFormData({...formData, doctor_name: e.target.value})}
              placeholder="Doctor name"
              style={{
                width: '100%',
                padding: '12px',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '14px'
              }}
            />
          </div>
        </div>

        {/* Mood */}
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
            Mood
          </label>
          <select
            value={formData.mood}
            onChange={(e) => setFormData({...formData, mood: e.target.value})}
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              fontSize: '14px',
              background: 'white'
            }}
          >
            <option value="excellent">😄 Excellent</option>
            <option value="good">😊 Good</option>
            <option value="okay">😐 Okay</option>
            <option value="low">😢 Low</option>
          </select>
        </div>

        {/* Symptoms */}
        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '12px' }}>
            Symptoms
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '8px' }}>
            {[
              { key: 'has_fever', label: '🤒 Fever' },
              { key: 'has_cough', label: '🤧 Cough' },
              { key: 'has_headache', label: '💢 Headache' },
              { key: 'has_fatigue', label: '😴 Fatigue' },
              { key: 'has_body_pain', label: '🤕 Body Pain' },
              { key: 'has_nausea', label: '🤢 Nausea' }
            ].map(symptom => (
              <label key={symptom.key} style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '8px',
                padding: '8px 12px',
                background: formData[symptom.key] ? '#e6fffa' : '#f8fafc',
                borderRadius: '8px',
                border: `1px solid ${formData[symptom.key] ? '#14b8a6' : '#e2e8f0'}`,
                cursor: 'pointer',
                fontSize: '12px'
              }}>
                <input
                  type="checkbox"
                  checked={formData[symptom.key]}
                  onChange={(e) => setFormData({...formData, [symptom.key]: e.target.checked})}
                  style={{ margin: 0 }}
                />
                {symptom.label}
              </label>
            ))}
          </div>
        </div>

        {/* Pain Level */}
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
            Pain Level
          </label>
          <select
            value={formData.pain_level}
            onChange={(e) => setFormData({...formData, pain_level: e.target.value})}
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              fontSize: '14px',
              background: 'white'
            }}
          >
            <option value="none">😌 None</option>
            <option value="mild">😐 Mild</option>
            <option value="moderate">😟 Moderate</option>
            <option value="severe">😰 Severe</option>
            <option value="critical">🚨 Critical</option>
          </select>
        </div>

        {/* Sleep Hours */}
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
            Sleep Hours
          </label>
          <input
            type="number"
            min="0"
            max="24"
            step="0.5"
            value={formData.sleep_hours}
            onChange={(e) => setFormData({...formData, sleep_hours: e.target.value})}
            placeholder="e.g., 7.5"
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              fontSize: '14px'
            }}
          />
        </div>

        {/* Sleep Quality */}
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
            Sleep Quality (1-10): {formData.sleep_quality}
          </label>
          <input
            type="range"
            min="1"
            max="10"
            value={formData.sleep_quality}
            onChange={(e) => setFormData({...formData, sleep_quality: parseInt(e.target.value)})}
            style={{ width: '100%' }}
          />
        </div>

        {/* Vitals */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '12px', marginBottom: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
              Temperature (°C)
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.temperature}
              onChange={(e) => setFormData({...formData, temperature: e.target.value})}
              placeholder="37.0"
              style={{
                width: '100%',
                padding: '12px',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '14px'
              }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
              BP Systolic
            </label>
            <input
              type="number"
              value={formData.blood_pressure_systolic}
              onChange={(e) => setFormData({...formData, blood_pressure_systolic: e.target.value})}
              placeholder="120"
              style={{
                width: '100%',
                padding: '12px',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '14px'
              }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
              BP Diastolic
            </label>
            <input
              type="number"
              value={formData.blood_pressure_diastolic}
              onChange={(e) => setFormData({...formData, blood_pressure_diastolic: e.target.value})}
              placeholder="80"
              style={{
                width: '100%',
                padding: '12px',
                border: '1px solid #e2e8f0',
                borderRadius: '8px',
                fontSize: '14px'
              }}
            />
          </div>
        </div>

        {/* Notes */}
        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
            Additional Notes
          </label>
          <textarea
            value={formData.notes}
            onChange={(e) => setFormData({...formData, notes: e.target.value})}
            placeholder="Any additional observations or notes..."
            rows={3}
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              fontSize: '14px',
              resize: 'vertical'
            }}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '12px',
            background: loading ? '#94a3b8' : 'linear-gradient(135deg, #14b8a6, #0d9488)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontWeight: 'bold',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? '⏳ Saving...' : '💾 Save Health Log'}
        </button>
      </form>
    </div>
  )
}
