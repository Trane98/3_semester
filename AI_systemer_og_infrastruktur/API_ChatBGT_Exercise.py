import requests
import base64
import os
import json

class APIChatGBT: 
    def __init__(self,
            url = "https://api.openai-proxy.org/v1/chat/completions",
            api_key = "sk-z3v9cFYsoEtYPSYX9QiExpv283o4QHqRnvy0eqqEcJOx8PK8@29301",
            content_type = "application/json",
            user_agent = "MyChatbot (Python 3.13; Windows 11; uni_env_3)"
    ):
        self.url = url
        self.api_key = api_key
        self.content_type = content_type
        self.user_agent = user_agent

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": self.content_type,
            "Accept": "text/event-stream",  # vi streamer altid
            "User-Agent": self.user_agent,
        }

    def encode_image(self, filepath):
        """Læser et lokalt billede og returnerer base64-strengen klar til API'et"""
        with open(filepath, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def send_message_streaming(self, conversation, model="gpt-4o-mini"):
        """Sender besked og streamer svaret"""
        data = {"model": model, "messages": conversation, "stream": True}

        try:
            with requests.post(
                self.url,
                headers=self.get_headers(),
                json=data,
                stream=True,
                timeout=30
            ) as response:
                response.raise_for_status()
                print("Assistant: ", end="", flush=True)
                full_answer = ""

                for line in response.iter_lines():
                    if line:
                        line = line.decode("utf-8")
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            try:
                                event_data = json.loads(data)

                                # Tjek at der faktisk er noget i choices
                                if "choices" in event_data and len(event_data["choices"]) > 0:
                                    delta = event_data["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        text = delta["content"]
                                        print(text, end="", flush=True)
                                        full_answer += text
                                # ellers ignorerer vi eventet
                            except json.JSONDecodeError:
                                continue

                print("\n")  # ny linje når streaming er færdig
                return full_answer

        except requests.exceptions.RequestException as e:
            print(f"Streaming request failed: {e}")
            return None


def main():
    bot = APIChatGBT(api_key="sk-z3v9cFYsoEtYPSYX9QiExpv283o4QHqRnvy0eqqEcJOx8PK8@29301")

    # Starter samtale
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]

    print("Velkommen til ChatGBT med billedunderstøttelse og streaming!")
    print("Skriv tekst som normalt, eller tilføj 'image:<sti>' for at sende tekst + billede i samme besked.")
    print("Eksempel: Tjek det her image:C:/Users/alex/Desktop/test.png")
    print("Skriv 'exit' for at afslutte.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Bygger content dynamisk (kan indeholde tekst + billede)
        content = []
        if "image:" in user_input:
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
            content.append({"type": "text", "text": user_input})

        # Tilføj brugerens besked til samtalen
        conversation.append({"role": "user", "content": content})

        # Send samtalen med streaming
        response = bot.send_message_streaming(conversation)

        if response:
            # Gem assistentens fulde svar i conversation
            conversation.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

