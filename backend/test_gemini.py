import requests

API_KEY = "AQ.Ab8RN6L4PN8fur6N6avuXuOeiX4erlQYmdrxLOFJobisEHLJDg"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "What is FastAPI?"
                }
            ]
        }
    ]
}

response = requests.post(
    url,
    json=payload,
    headers={"Content-Type": "application/json"}
)

print("Status Code:", response.status_code)
print(response.text)