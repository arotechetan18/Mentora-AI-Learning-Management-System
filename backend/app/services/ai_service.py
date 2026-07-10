import os
import requests
from ..core.config import settings

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = "gemini-pro"
    
    def get_answer(self, question: str, context: str = None) -> str:
        """Get AI response for student doubt"""
        try:
            prompt = f"""You are an AI tutor for a Learning Management System.
            Answer the following question clearly and accurately.
            
            Context: {context if context else "General"}
            Question: {question}
            
            Provide a helpful, educational response.
            """
            
            url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "I apologize, but I'm unable to answer your question at the moment."
        except Exception as e:
            return f"Error: {str(e)}"