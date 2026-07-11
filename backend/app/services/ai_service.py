import requests
from ..core.config import settings


class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = "gemini-flash-latest"

    def get_answer(self, question: str, context: str = None) -> str:
        try:
            prompt = f"You are an AI tutor.\n\nQuestion: {question}"

            if context:
                prompt += f"\n\nContext:\n{context}"

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(
    url,
    json=payload,
    headers={"Content-Type": "application/json"},
    timeout=30
)

            if response.status_code == 200:
                data = response.json()

                return data["candidates"][0]["content"]["parts"][0]["text"]

            return f"Error {response.status_code}: {response.text}"

        except requests.exceptions.RequestException as e:
              print(e)
              return str(e)