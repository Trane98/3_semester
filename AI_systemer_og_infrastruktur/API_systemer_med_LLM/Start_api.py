from API_functions import API, chatbot
import requests
import json
import base64



client = API()

# Tekstmodel
chatbot(client, model="llava")

# Multimodal model (kan tilføje billeder med addimg path)
# chatbot(client, model="llava")
