# main.py
from controllerCriarGrupo import Controlador
import os

# Configurar caminhos para arquivos dentro da pasta viana
DIR_VIANA = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    'MAX_GRUPO': 5,
    'PESO_CURSO': 2,
    'PESO_DISCIPLINA': 3,
    'PESO_PERIODO': 1,
    'DADOS_PATH': os.path.join(DIR_VIANA, 'Estudantes.csv'),
    'GRUPOS_PATH': os.path.join(DIR_VIANA, 'grupos_estudo.csv')
}

if __name__ == "__main__":
    controlador_app = Controlador(CONFIG)
    controlador_app.executar_montagem_de_grupo()