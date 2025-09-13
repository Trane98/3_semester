import requests
import base64
import os

class APIChatGBT: 
    def __init__(self,
            url = "https://api.openai-proxy.org/v1/chat/completions",
            api_key = "sk-z3v9cFYsoEtYPSYX9QiExpv283o4QHqRnvy0eqqEcJOx8PK8@29301",
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

            usage = result.get("usage", {})
            print(f"\nPrompt tokens: {usage.get('prompt_tokens')}")
            print(f"Completion tokens: {usage.get('completion_tokens')}")
            print(f"Total tokens: {usage.get('total_tokens')}")
            return answer
        else:
            print("Fejl:", response.status_code, response.text)
            return None


def main():
    bot = APIChatGBT(api_key = "sk-z3v9cFYsoEtYPSYX9QiExpv283o4QHqRnvy0eqqEcJOx8PK8@29301")

    # Starter samtale
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("Velkommen til ChatGBT med billedunderstøttelse!")
    print("Skriv tekst som normalt, eller skriv 'image:<sti>' for at sende et billede.")
    print("Skriv 'exit' for at afslutte.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Bygger content dynamisk
        content = []
        if user_input.startswith("image:"):
            # Brugeren har skrevet en sti til et billede
            filepath = user_input.split("image:")[1].strip()
            if os.path.exists(filepath):
                img_b64 = bot.encode_image(filepath)
                content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}})
            else:
                print("Billedsti ikke fundet!")
                continue
        else:
            # Almindelig tekst
            content.append({"type": "text", "text": user_input})

        # Tilføj brugerens besked
        conversation.append({"role": "user", "content": content})

        # Send hele samtalen
        response = bot.send_message(conversation)
        if response:
            conversation.append({"role": "assistant", "content": response})


main()
