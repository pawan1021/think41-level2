import os
import requests

def generate_response(prompt: str) -> str:
    GROQ_API_KEY = os.getenv("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")
    if not GROQ_API_KEY:
        return "LLM API key is missing."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result['choices'][0]['message']['content']
