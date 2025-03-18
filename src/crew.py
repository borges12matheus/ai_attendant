from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()
serper_key=os.getenv("SERPER_API_KEY")
llm_model=os.getenv("MODEL")
llm_key=os.getenv("GEMINI_API_KEY")

llm = LLM(model=llm_model,
          api_key=llm_key)

search_tool = SerperDevTool()

# Agente: Atendente Virtual
atendente_virtual = Agent(
    role="Atendente Virtual",
    goal="Responder dúvidas dos usuários contido no texto {msg_text} da melhor forma possível.",
    backstory=(
        "Você é um atendente virtual altamente treinado, capaz de responder dúvidas  "
        "sobre diversos assuntos. Caso não tenha certeza da resposta, você pode "
        "pedir ajuda para um pesquisador especializado."
    ),
    verbose=True,
    llm=llm,
    memory=True,
    allow_delegation=True  # Permite delegar tarefas ao pesquisador
)

# Agente: Pesquisador
pesquisador = Agent(
    role="Pesquisador Web",
    goal="Buscar informações na internet para responder dúvidas com precisão.",
    backstory=(
        "Você é um especialista em buscas na web. Quando recebe uma pergunta, "
        "utiliza sua ferramenta de busca para encontrar informações confiáveis e precisas."
    ),
    tools=[search_tool],  # Usa a ferramenta de busca
    llm=llm,
    verbose=True,
    memory=True
)

# Tarefa do atendente virtual
tarefa_atendente = Task(
    description=(
        "Receber a pergunta do usuário e tentar responder com base no seu conhecimento. "
        "Caso não saiba a resposta, delegue a tarefa para o Pesquisador Web."
    ),
    expected_output="Uma resposta clara e objetiva para a pergunta do usuário.",
    agent=atendente_virtual
)

# Tarefa do pesquisador
tarefa_pesquisador = Task(
    description=(
        "Pesquisar na internet a resposta para a pergunta do usuário {msg_text} e fornecer um resumo da melhor resposta encontrada."
    ),
    expected_output="Um resumo objetivo com a melhor informação disponível sobre a pergunta.",
    agent=pesquisador
)

# Criando a equipe (Crew)
crew = Crew(
    agents=[atendente_virtual, pesquisador],
    tasks=[tarefa_atendente, tarefa_pesquisador],
    process=Process.sequential  # Executa as tarefas em sequência
)

def run(msg):
    print(msg)
    return crew.kickoff(inputs={'msg_text':msg})

#print(run(msg = "O que é tcc?"))