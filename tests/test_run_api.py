import requests
import json
OPENROUTER_DEEPSEEK_API_KEY="YOUR_API_KEY"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENROUTER_DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "model": "deepseek/deepseek-r1-0528:free",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "stream": False,
    "temperature": 0.8,
    "max_tokens": 10000,
    "response_format": "json_object",
    "include_reasoning": True
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response.json()['choices'][0]['message']['reasoning'])