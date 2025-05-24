from notificacao import Notificacao

class Grupo:
    def __init__(self, materia):
        self.materia = materia
        self.membros = []

    def adicionar_membro(self, perfil):
        if perfil not in self.membros:
            self.membros.append(perfil)
            perfil.receber_notificacao(f"Você foi adicionado ao grupo de '{self.materia}'.")
            for m in self.membros:
                if m != perfil:
                    m.receber_notificacao(f"{perfil.nome} entrou no grupo de '{self.materia}'.")
