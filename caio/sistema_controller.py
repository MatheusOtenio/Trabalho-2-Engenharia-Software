import csv
import os
from perfil import Perfil
from grupo import Grupo

# Garantir que todos os arquivos sejam criados dentro da pasta caio
DIR_CAIO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(DIR_CAIO, "usuarios.csv")

class SistemaController:
    _instance = None

    @staticmethod
    def get_instance():
        if SistemaController._instance is None:
            SistemaController._instance = SistemaController()
        return SistemaController._instance

    def __init__(self):
        if SistemaController._instance is not None:
            raise Exception("Use SistemaController.get_instance() para obter a instância.")
        self.usuarios = self.carregar_usuarios()
        self.grupos = {}

    def carregar_usuarios(self):
        usuarios = []
        if not os.path.exists(ARQUIVO_CSV):
            return usuarios
        with open(ARQUIVO_CSV, "r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                usuarios.append(Perfil(
                    row["nome"],
                    row["ra"],
                    row["email"],
                    row["materias"].split(";") if row["materias"] else [],
                    row["amigos"].split(";") if row["amigos"] else [],
                    int(row["grupos"])
                ))
        return usuarios

    def salvar_usuarios(self):
        with open(ARQUIVO_CSV, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ra", "nome", "email", "materias", "amigos", "grupos"])
            for u in self.usuarios:
                writer.writerow([
                    u.ra,
                    u.nome,
                    u.email,
                    ";".join(u.materias_interesse),
                    ";".join(u.amigos),
                    u.grupos_participados
                ])

    def buscar_usuario(self, ra):
        for u in self.usuarios:
            if u.ra == ra:
                return u
        return None

    def adicionar_usuario(self, perfil):
        self.usuarios.append(perfil)
        self.salvar_usuarios()

    def adicionar_usuario_ao_grupo(self, usuario, materia):
        if materia not in self.grupos:
            self.grupos[materia] = Grupo(materia)
        self.grupos[materia].adicionar_membro(usuario)
        usuario.grupos_participados += 1
