import requests
import base64

class APIChatGBT: 
    def __init__(self,
            url = "https://api.openai-proxy.org/v1/chat/completions",
            api_key = "DIN_API_KEY_HER",
            content_type = "application/json",
            accept = "application/json",
            user_agent = "MyChatbot (Python 3.13; Windows 11; uni_env_3)"
    ):
        self.url = url
        self.api_key = api_key
        self.content_type = content_type
        self.accept = accept
        self.user_agent = user_agent

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": self.content_type,
            "Accept": self.accept,
            "User-Agent": self.user_agent,
        }

    def encode_image(self, filepath):
        """Læser et lokalt billede og returnerer base64-strengen klar til API'et"""
        with open(filepath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def send_message(self, conversation, model="gpt-4o-mini"):
        data = {
            "model": model,
            "messages": conversation
        }

        response = requests.post(url=self.url, headers=self.get_headers(), json=data)

        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            print("Assistant:", answer)

            # token-forbrug
            usage = result.get("usage", {})
            print(f"\nPrompt tokens: {usage.get('prompt_tokens')}")
            print(f"Completion tokens: {usage.get('completion_tokens')}")
            print(f"Total tokens: {usage.get('total_tokens')}")
            return answer
        else:
            print("Fejl:", response.status_code, response.text)
            return None


def main():
    bot = APIChatGBT(api_key="DIN_API_KEY_HER")

    # Samtale starter laver strukturen til API'et
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    # Først sender vi et billede med et spørgsmål
    img_b64 = bot.encode_image("kat.png")
    conversation.append({
        "role": "user",
        "content": [
            {"type": "text", "text": "Kan du beskrive det her billede?"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
        ]
    })

    response = bot.send_message(conversation)

    # Tilføj assistentens svar
    conversation.append({"role": "assistant", "content": response})

    # Så kan du fortsætte dialogen
    conversation.append({"role": "user", "content": "Okay, hvilken race tror du katten er?"})
    response = bot.send_message(conversation)
    conversation.append({"role": "assistant", "content": response})


main()
