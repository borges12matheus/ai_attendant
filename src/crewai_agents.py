from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()
serper_key=os.getenv("SERPER_API_KEY")
llm_model=os.getenv("MODEL")
llm_key=os.getenv("DEEPSEEK_API_KEY")

llm = LLM(model=llm_model,
          api_key=llm_key)

search_tool = SerperDevTool()

# Agente: Atendente Virtual
atendente_virtual = Agent(
    role="Agente de Atendimento Inicial",
    goal="Responder cordialmente clientes do WhatsApp e entender suas intenções com base em na mensagem enviada: {msg}",
    backstory=(
        '''Você é um assistente virtual da Concorde Viagens. Sua missão é oferecer um atendimento caloroso,
            entender o que o cliente deseja e direcioná-lo conforme a orientação do especialista.
            Você irá finalizar o atendimento assim que todas as informações necessárias forem coletadas.
            O orçamento será feito por um consultor especialista em viagens, portanto,
            deve informar o cliente que o consultor entrará em contato em breve para apresentar o orçamento.'''
    ),
    verbose=True,
    llm=llm,
    memory=True,
    allow_delegation=True
)

# Agente: especialista_triagem
especialista_triagem = Agent(
    role="Especialista em Triagem de Viagem",
    goal="Coletar dados essenciais da solicitação do cliente.",
    backstory=(
        '''Você atua como um especialista em entender o que o cliente quer, seja uma viagem, pacote ou dúvidas.
            Seu foco é coletar destino, datas, número de pessoas, orçamento e outras informações relevantes, para então,
            repassar essas informações para um consultor especialista que irá realizar o orçamento.
            Portanto, você deve coletar todas as informações necessárias para fazer o orçamento, porém você não irá fazer o orçamento.'''
    ),
    #tools=[search_tool],  # Usa a ferramenta de busca
    llm=llm,
    verbose=True,
    memory=True
)

# Agente: especialista_triagem
supervisor_respostas = Agent(
    role="Supervisor de Respostas para Comunicação com Cliente",
    goal="Garantir que todas as mensagens enviadas ao cliente sejam simples, claras e compreensíveis.",
    backstory=(
        '''Você é um revisor rigoroso da Concorde Viagens. Sua missão é revisar as mensagens que serão enviadas
            aos clientes e garantir que estejam compreensíveis, bem escritas e respondam exatamente o que foi solicitado.
            Se estiver confuso ou técnico demais, solicite reformulação ao especialista. Se faltar informação,
            peça ao cliente de forma educada para completar.'''
    ),
    llm=llm,
    verbose=True,
    memory=True
)


# Tarefa do atendente virtual
atendimento_inicial = Task(
    description=(
        '''Receba a mensagem do cliente via WhatsApp e descubra qual o motivo do contato:
            compra de passagem, pacotes, dúvidas, etc.
            Seja sempre cordial e use linguagem informal mas respeitosa.'''
    ),
    expected_output="Uma mensagem respondida e a intenção identificada do cliente: [passagem, pacote, dúvida, etc].",
    agent=atendente_virtual
)

# Tarefa do especialista em triagem
triagem_de_dados = Task(
    description=(
        '''Coletar as seguintes informações do cliente com base na intenção identificada:
            - Destino
            - Datas de ida e volta
            - Número de pessoas
            - Orçamento estimado
            - Alguma preferência de voo ou hospedagem
            Seja amigável, guiando com perguntas diretas.
            OBSERVAÇÃO: Caso o cliente não forneça nenhuma informação que possibilite fazer a triagem, 
            você deve retornar solicitando mais informações'''
    ),
    expected_output="Um conjunto organizado de dados da viagem do cliente, pronto para ser armazenado.",
    agent=especialista_triagem
)

supervisao_resposta = Task(
    description=(
        '''Verifique se a resposta do Especialista em Triagem está clara e compreensível para o cliente.
            Se a resposta estiver confusa ou com termos técnicos, solicite reformulação ao Especialista.
            Se faltar informação essencial, peça diretamente ao cliente com uma pergunta clara e objetiva.'''
    ),
    expected_output='''Uma mensagem final validada, clara e compreensível, pronta para ser enviada ao cliente.
                        Se necessário, uma solicitação de reformulação ao Especialista 
                        ou uma nova pergunta ao cliente.''' ,
    agent=supervisor_respostas
)

# Tarefa do atendente virtual
envio_mensagem_ao_cliente = Task(
    description=(
        '''Após a validação da mensagem pelo Supervisor de Respostas, envie essa mensagem final ao cliente
            utilizando o canal oficial da Concorde Viagens no WhatsApp. Mantenha a cordialidade e a simplicidade.'''
    ),
    expected_output="Confirmação de que a mensagem foi enviada com sucesso ao cliente.",
    agent=atendente_virtual
)

# Criando a equipe (Crew)
crew = Crew(
    agents=[atendente_virtual, especialista_triagem, supervisor_respostas],
    tasks=[atendimento_inicial, triagem_de_dados, envio_mensagem_ao_cliente],
    process=Process.sequential  # Executa as tarefas em sequência
)

def run(msg):
    print(msg)
    return crew.kickoff(inputs={'msg':msg})