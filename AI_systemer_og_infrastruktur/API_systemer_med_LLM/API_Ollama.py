import requests
import json
import os
import base64

url = "http://localhost:11434/api/generate"
# (Ollama kræver det ikke, men princippet bliver vist)
API_KEY = os.getenv("OLLAMA_API_KEY", "FAKE_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}", # Falsk API-nøgle da Ollama ikke kræver autentificering
    "Content-Type": "application/json", # Fortæller serveren, at vi sender JSON data
    "Accept": "application/json", # Fortæller serveren, at vi forventer JSON data tilbage
    "User-Agent": "MyChatbotOllama (Python 3.13; Windows 10; uni_env_3)", # Identificerer vores klient til serveren
}

conversation = []


print("Welcome to the Ollama API Chatbot! You can exit the chat by typing 'exit' or 'quit'.")
choice = input("Which model? Press 1 for llava (Picture Analytic AI), 2 for llama3.1 (text based) or 3 for llama3 (text based): ")

if choice == "1":
    current_model = "llava"
elif choice == "2":
    current_model = "llama3.1:8b"
elif choice == "3":
    current_model = "llama3"
else:
    print("Invalid choice, defaulting to llava.")
    current_model = "llava"

if current_model == "llama3" or current_model == "llama3.1:8b":
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            break

        # Tilføjer brugerinput til samtalen
        conversation.append(f"You: {user_input}")

        # Kombiner hele historikken som en prompt
        full_prompt = "\n".join(conversation)

        payload = {
                "model": current_model,
                "prompt": full_prompt,
                "stream": False
        }



        response = requests.post(url, headers=headers, json=payload)

        # Kontrollerer om anmodningen var succesfuld
        if response.status_code == 200:
            print(f"\nResponse received from Ollama API. Responding AI = {current_model}\n")

            data = response.json()
            model_reply = data["response"]
            prompt_tokens = data.get("prompt_eval_count")
            response_tokens = data.get("eval_count")


            # Tilføj modellens svar til samtalen
            conversation.append(f"Assistant: {model_reply}")

            print(f"Assistant: {model_reply}\n")
            print(f"Prompt tokens used: {prompt_tokens}")
            print(f"Response tokens used: {response_tokens}")

        # Print fejlmeddelelse hvis anmodningen mislykkes
        else:
            print("Something went wrong. Look at the error message below:")
            print("Error:", response.status_code, response.text)

elif current_model == "llava":
    while True: 
        user_input = input("\nPlease input image path and question (separated by a comma): ")

        if user_input.lower() in ["exit", "quit"]:
            break

        # Split input i [sti, spørgsmål]
        try:
            image_path, question = [x.strip() for x in user_input.split(",", 1)]
        except ValueError:
            print("Husk at skrive: <image_path>, <question>")
            continue

        # Læs billedet og konverter til base64
        with open(image_path, "rb") as f:
            img_bytes = f.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # Tilføjer input til samtalen
        conversation.append(f"You: {question}")

        # Kombiner hele historikken som prompt
        full_prompt = "\n".join(conversation)

        payload = {
            "model": current_model,
            "prompt": full_prompt,
            "images": [img_base64],
            "stream": False
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print(f"\nResponse received from Ollama API. Responding AI = {current_model}\n")

            data = response.json()
            model_reply = data["response"]
            prompt_tokens = data.get("prompt_eval_count")
            response_tokens = data.get("eval_count")

            conversation.append(f"Assistant: {model_reply}")

            print(f"Assistant: {model_reply}\n")
            print(f"Prompt tokens used: {prompt_tokens}")
            print(f"Response tokens used: {response_tokens}")

        else:
            print("Something went wrong. Look at the error message below:")
            print("Error:", response.status_code, response.text)
