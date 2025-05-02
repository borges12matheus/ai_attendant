from flask import Flask, request
from message_interpreter import MessageReceiver
from sender_message import SendMessage
from crewai_agents import run

app = Flask(__name__)

@app.route("/messages-upsert", methods=['POST'])

def funcao():
    data = request.get_json()
    msg = MessageReceiver(data)
    print(f"\nMensagem:{msg.text_message} - enviado por:{msg.phone}\n")
    resultado = run(msg.text_message)
    print(resultado)
    sender = SendMessage()
    sender.text(number=msg.phone, msg=str(resultado))
    print("Messagem enviada")
    return "Evolution Iniciado"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000",debug=True)