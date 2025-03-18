import os
from dotenv import load_dotenv
from evolutionapi.client import EvolutionClient
from evolutionapi.models.message import TextMessage, MediaMessage

load_dotenv()

evo_api_token = os.getenv("EVO_API_TOKEN")
evo_instance_id = os.getenv("EVO_INSTANCE_NAME")
evo_instance_token = os.getenv("EVO_INSTANCE_TOKEN")

#Instanciando o EvolutionClient
client = EvolutionClient(
    base_url= 'http://localhost:8081',
    api_token=evo_api_token
)

#Criando uma mensagem de Texto
text_message = TextMessage(
    number="55xxxxxxxxxx",
    text="Olá, estou enviando esta mensagem via Evolution API"
)

#Enviando a mensagem
response = client.messages.send_text(evo_instance_id,
                                     text_message,
                                     evo_instance_token)

print(response)