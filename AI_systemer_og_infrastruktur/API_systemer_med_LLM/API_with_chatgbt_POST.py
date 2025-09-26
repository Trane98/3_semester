import requests
import json

api_key = "sk-ZWUeRmQA3uV3MZgf98Nmu7jpFayw4M84iQssF5LtefhKq8Tw@29301"

url = "https://api.openai-proxy.org/v1/chat/completions"

# Headers vi sender med vores request giver os adgang til API'en og fortæller hvad vi sender og ønsker at modtage
headers = {
    "Authorization": f"Bearer {api_key}", # Identificerer os overfor API'en med en API-nøgle
    "Content-Type": "application/json", # Angiver at vi sender JSON data
    "Accept": "application/json", # Angiver at vi ønsker at modtage JSON data
    "User-Agent": "MyChatbot (Python 3.13; Windows 11; uni_env_3)" # Identificerer vores klient og vores python version samt miljø
}

# Data vi sender til API'en
data = {
    "model": "gpt-4o-mini", # Vores model valg
    "messages": [
        {"role": "user", "content": "Hello! How are you?"} # Hvad vi siger til modellen
    ]
}

# Gør klar til at sende vores request og modtage et svar
response = requests.post(url, headers=headers, json=data) 

if response.status_code == 200:
    result = response.json()
    print("Model svar:", result["choices"][0]["message"]["content"])
else:
    print("Fejl:", response.status_code, response.text)
