from openai import OpenAI
from typing import List, Dict
from datetime import datetime, timedelta

from app.config import settings
from app.models.healthlog_model import HealthLog
from app.models.user_model import User

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class AIService:
    """AI-powered health insights service"""
    
    @staticmethod
    async def analyze_health_trends(user: User, logs: List[HealthLog]) -> Dict:
        """Analyze health trends and provide insights"""
        
        if not logs:
            return {
                "insights": "No health data available for analysis. Start logging your daily health to get personalized insights.",
                "recommendations": [],
                "correlations": []
            }
        
        # Prepare data summary for AI
        log_summary = AIService._prepare_log_summary(logs)
        
        # Create prompt
        prompt = f"""
You are a health analyst AI. Analyze the following health data and provide insights.

Patient Information:
- Name: {user.full_name}
- Blood Group: {user.blood_group or 'Not specified'}
- Allergies: {', '.join(user.allergies) if user.allergies else 'None'}
- Chronic Conditions: {', '.join(user.chronic_conditions) if user.chronic_conditions else 'None'}

Health Logs Summary (Last {len(logs)} entries):
{log_summary}

Please provide:
1. Key health trends observed
2. Correlations between symptoms and lifestyle factors (e.g., sleep and headaches)
3. 3-5 actionable health recommendations
4. Any concerning patterns that need medical attention

Format your response as JSON with keys: "trends", "correlations", "recommendations", "alerts"
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful health analysis assistant. Provide clear, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            insights_text = response.choices[0].message.content
            
            return {
                "insights": insights_text,
                "data_points_analyzed": len(logs),
                "analysis_date": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"AI analysis failed: {str(e)}",
                "insights": "Unable to generate insights at this time."
            }
    
    
    @staticmethod
    def _prepare_log_summary(logs: List[HealthLog]) -> str:
        """Prepare a text summary of health logs"""
        summary_lines = []
        
        for i, log in enumerate(logs[:30], 1):  # Last 30 logs
            log_info = f"Day {i} ({log.log_date.strftime('%Y-%m-%d')}):"
            
            details = []
            if log.temperature:
                details.append(f"Temp: {log.temperature}°F")
            if log.sleep_hours:
                details.append(f"Sleep: {log.sleep_hours}hrs")
            if log.mood:
                details.append(f"Mood: {log.mood.value}")
            
            symptoms = []
            if log.has_fever:
                symptoms.append("fever")
            if log.has_headache:
                symptoms.append("headache")
            if log.has_cough:
                symptoms.append("cough")
            if log.has_fatigue:
                symptoms.append("fatigue")
            
            if symptoms:
                details.append(f"Symptoms: {', '.join(symptoms)}")
            
            if details:
                log_info += " " + ", ".join(details)
            
            summary_lines.append(log_info)
        
        return "\n".join(summary_lines)
    
    
    @staticmethod
    async def get_symptom_advice(symptom: str, severity: str = "mild") -> Dict:
        """Get AI advice for specific symptom"""
        
        prompt = f"""
A patient is experiencing {symptom} with {severity} severity.

Provide:
1. Possible causes (3-4 common ones)
2. Home remedies and self-care tips
3. When to see a doctor (red flags)
4. Prevention tips

Keep it concise and practical. Format as JSON with keys: "causes", "remedies", "when_to_see_doctor", "prevention"
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical information assistant. Provide general health advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            advice = response.choices[0].message.content
            
            return {
                "symptom": symptom,
                "severity": severity,
                "advice": advice,
                "disclaimer": "This is general information only. Consult a healthcare professional for medical advice."
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get advice: {str(e)}"
            }
    
    
    @staticmethod
    async def chat_with_health_assistant(user: User, message: str, conversation_history: List[Dict] = None) -> Dict:
        """Chat with AI health assistant"""
        
        if conversation_history is None:
            conversation_history = []
        
        # Build conversation
        messages = [
            {"role": "system", "content": f"""You are a friendly health assistant helping {user.full_name}. 
            Provide helpful health information, answer questions about symptoms, healthy lifestyle, and general wellness.
            Always remind users to consult healthcare professionals for medical decisions.
            Be empathetic and supportive."""}
        ]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Last 5 messages
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.8,
                max_tokens=300
            )
            
            assistant_reply = response.choices[0].message.content
            
            return {
                "response": assistant_reply,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Chat failed: {str(e)}",
                "response": "I'm having trouble responding right now. Please try again."
            }
