from notificacao import Notificacao

class Perfil:
    def __init__(self, nome, ra, email, materias=None, amigos=None, grupos=0):
        self.nome = nome
        self.ra = ra
        self.email = email
        self.materias_interesse = materias if materias else []
        self.amigos = amigos if amigos else []
        self.grupos_participados = grupos
        self.notificacoes = []

    def adicionar_materia(self, materia):
        if materia not in self.materias_interesse:
            self.materias_interesse.append(materia)

    def adicionar_amigo(self, ra_amigo):
        if ra_amigo not in self.amigos:
            self.amigos.append(ra_amigo)

    def remover_amigo(self, ra_amigo):
        if ra_amigo in self.amigos:
            self.amigos.remove(ra_amigo)

    def receber_notificacao(self, mensagem):
        self.notificacoes.append(Notificacao(mensagem))
