import requests
import json
import base64


class API:
    def __init__(
        self,
        url="http://localhost:11434/api/generate",
        api_key="FAKE_KEY",
        content_type="application/json",
        accept="application/json",
        user_agent="MyChatbotOllama (Python 3.13; Windows 10; uni_env_3)",
    ):
        self.url = url
        self.api_key = api_key
        self.content_type = content_type
        self.accept = accept
        self.user_agent = user_agent

    def get_headers(self):
        """Generates headers for the API request depending on the instance attributes."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": self.content_type,
            "Accept": self.accept,
            "User-Agent": self.user_agent,
        }

    def generate(self, model, prompt, images=None, stream=False):
        """Send request to Ollama API. Supports text and multimodal input."""
        payload = {"model": model, "prompt": prompt, "stream": stream}
        if images:
            payload["images"] = images
        response = requests.post(self.url, headers=self.get_headers(), json=payload)
        return response

    @staticmethod
    def encode_image(path):
        """Helper to convert an image to base64 string for LLaVA."""
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")


def chatbot(api, model="llama3"):
    conversation = []
    images = []

    print("Welcome to the Chatbot! Type 'exit' to quit, or 'addimg <path>' to send an image.\n")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        # Hvis brugeren tilføjer et billede
        if user_input.startswith("addimg "):
            path = user_input.split(" ", 1)[1]
            try:
                images.append(API.encode_image(path))  # nu staticmethod
                print(f"[Image added: {path}]")
            except FileNotFoundError:
                print(f"[Error: could not find {path}]")
            continue

        # Tilføj tekst til samtalen
        conversation.append(f"You: {user_input}")
        full_prompt = "\n".join(conversation)

        # Lav API-kaldet
        response = api.generate(model, full_prompt, images=images)
        if response.status_code == 200:
            data = response.json()
            reply = data["response"]
            conversation.append(f"Assistant: {reply}")

            print(f"\nAssistant: {reply}\n")
            print(f"Prompt tokens used: {data.get('prompt_eval_count')}")
            print(f"Response tokens used: {data.get('eval_count')}")
        else:
            print(f"Error: {response.status_code}, {response.text}")