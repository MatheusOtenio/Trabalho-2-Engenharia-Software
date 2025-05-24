# main.py
from controllerCriarGrupo import Controlador

CONFIG = {
    'MAX_GRUPO': 5,
    'PESO_CURSO': 2,
    'PESO_DISCIPLINA': 3,
    'PESO_PERIODO': 1,
    'DADOS_PATH': 'Estudantes.csv',
    'GRUPOS_PATH': 'grupos_estudo.csv'
}

if __name__ == "__main__":
    controlador_app = Controlador(CONFIG)
    controlador_app.executar_montagem_de_grupo()