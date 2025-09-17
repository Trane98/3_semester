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
            message = result["choices"][0]["message"]

            # Håndterer svar (tekst eller liste)
            answer = ""
            if isinstance(message["content"], str):
                answer = message["content"]
            elif isinstance(message["content"], list):
                parts = []
                for item in message["content"]:
                    if item["type"] == "text":
                        parts.append(item["text"])
                    elif item["type"] == "image_url":
                        parts.append(f"[Billede: {item['image_url']['url']}]")
                answer = "\n".join(parts)

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
    bot = APIChatGBT(api_key="sk-z3v9cFYsoEtYPSYX9QiExpv283o4QHqRnvy0eqqEcJOx8PK8@29301")

    # Starter samtale
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("Velkommen til ChatGBT med billedunderstøttelse!")
    print("Skriv tekst som normalt, eller tilføj 'image:<sti>' for at sende tekst + billede i samme besked.")
    print("Eksempel: Se det her image:C:/Users/alex/Desktop/test.png")
    print("Skriv 'exit' for at afslutte.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Bygger content dynamisk (kan indeholde tekst + billede i samme besked)
        content = []
        if "image:" in user_input:
            # Split input i tekst og billedsti
            parts = user_input.split("image:")
            text_part = parts[0].strip()
            img_path = parts[1].strip()

            if text_part:
                content.append({"type": "text", "text": text_part})

            if os.path.exists(img_path):
                img_b64 = bot.encode_image(img_path)
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                })
            else:
                print("Billedsti ikke fundet!")
                continue
        else:
            # Kun tekst
            content.append({"type": "text", "text": user_input})

        # Tilføj brugerens besked til conversation
        conversation.append({"role": "user", "content": content})

        # Send samtalen
        response = bot.send_message(conversation)
        if response:
            conversation.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
