import requests

api_key = "sk-ZWUeRmQA3uV3MZgf98Nmu7jpFayw4M84iQssF5LtefhKq8Tw@29301"
url = "https://api.openai-proxy.org/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    result = response.json()
    print("Tilgængelige modeller:", [m["id"] for m in result["data"]])
else:
    print("Fejl:", response.status_code, response.text)


# Generelt så er en GET request brugt til at hente information fra en server, mens en POST request bruges til at sende data til en server for at skabe eller opdatere ressourcer.
# Så i dette tilfælde bruger vi en GET request fordi vi ønsker at hente en liste over tilgængelige modeller fra API'en.