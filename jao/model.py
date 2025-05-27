# model.py

# Model (Parte do MVC)
# Este arquivo contém as classes de modelo que representam as entidades do sistema

# Model: Estruturas de dados do sistema

class Question:
    # Classe para armazenar perguntas do fórum
    def __init__(self, id, ra, user, text):
        self.id = id          # ID único da pergunta
        self.ra = ra          # RA do usuário
        self.user = user      # Nome do usuário
        self.text = text      # Texto da pergunta
        self.answers = []     # Lista de respostas

class Answer:
    # Classe para armazenar respostas às perguntas
    def __init__(self, question_id, responder_ra, responder_name, text):
        self.question_id = question_id        # ID da pergunta relacionada
        self.responder_ra = responder_ra      # RA do respondente
        self.responder_name = responder_name  # Nome do respondente
        self.text = text                      # Texto da resposta