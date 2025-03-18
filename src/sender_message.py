import os
from dotenv import load_dotenv
from evolutionapi.client import EvolutionClient
from evolutionapi.models.message import TextMessage, MediaMessage

class SendMessage:
    
    def __init__ (self) -> None:
        #Carrega as variáveis e tokens
        load_dotenv()
        self.evo_api_token = os.getenv("EVO_API_TOKEN")
        self.evo_instance_id = os.getenv("EVO_INSTANCE_NAME")
        self.evo_instance_token = os.getenv("EVO_INSTANCE_TOKEN")
        self.evo_base_url = os.getenv("EVO_BASE_URL")

        #Instanciando o EvolutionClient
        self.client = EvolutionClient(
            base_url= self.evo_base_url,
            api_token=self.evo_api_token
        )
    
    def text(self, number, msg , metions=[]):
        #Criando uma mensagem de Texto
        text_message = TextMessage(
            number=str(number),
            text=msg
        )

        #Enviando a mensagem
        response = self.client.messages.send_text(
            self.evo_instance_id,
            text_message,
            self.evo_instance_token
            )
        return response
    
    def pdf(self, number , pdf_file, caption=""):
        #Enviar um PDF
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"Arquivo '{pdf_file}' não encontrado!")
        
        pdf_message = MediaMessage(
            number=number,
            mediatype="document",
            mimetype="application/pdf",
            caption=caption,
            fileName=os.path.basename(pdf_file),
            media=""
        )
         #Enviando o PDF
        self.client.messages.send_media(
            self.evo_instance_id,
            pdf_message,
            self.evo_instance_token,
            pdf_file
            )
        return "PDF Enviado"
        
    def audio(self, number , audio_file):
        #Enviar um áudio
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Arquivo '{audio_file}' não encontrado!")
        
        audio_message = {
            "number": number,
            "mediatype": "audio",
            "mimetype": "audio/mpeg",
            "caption": ""
        }
        
        #Enviando o áudio
        self.client.messages.send_whatsapp_audio(
            self.evo_instance_id,
            audio_message,
            self.evo_instance_token,
            audio_file
            )
        
        return "Áudio Enviado"
    
    def image(self, number , image_file, caption=""):
        #Enviar uma imagem
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"Arquivo '{image_file}' não encontrado!")
        
        image_message = MediaMessage(
            number=number,
            mediatype="image",
            mimetype="image/jpeg",
            caption=caption,
            fileName=os.path.basename(image_file),
            media=""
        )
         #Enviando a Imagem
        self.client.messages.send_media(
            self.evo_instance_id,
            image_message,
            self.evo_instance_token,
            image_file
            )
        return "Imagem Enviada"
    
    def video(self, number , video_file, caption=""):
        #Enviar um vídeo
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Arquivo '{video_file}' não encontrado!")
        
        video_message = MediaMessage(
            number=number,
            mediatype="video",
            mimetype="video/mp4",
            caption=caption,
            fileName=os.path.basename(video_file),
            media=""
        )
         #Enviando a Imagem
        self.client.messages.send_media(
            self.evo_instance_id,
            video_message,
            self.evo_instance_token,
            video_file
            )
        return "Vídeo Enviado"
    
    def document(self, number , doc_file, caption=""):
    #Enviar um documento
        if not os.path.exists(doc_file):
            raise FileNotFoundError(f"Arquivo '{doc_file}' não encontrado!")
        
        doc_message = MediaMessage(
            number=number,
            mediatype="document",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            caption=caption,
            fileName=os.path.basename(doc_file),
            media=""
        )
         #Enviando a Imagem
        self.client.messages.send_media(
            self.evo_instance_id,
            doc_message,
            self.evo_instance_token,
            doc_file
            )
        return "Documento Enviado"