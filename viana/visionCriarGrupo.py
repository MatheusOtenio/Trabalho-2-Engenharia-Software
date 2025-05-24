# view.py
import pandas as pd

class Visao:
    def update(self, event_type, data_payload=None):
  
        # print(f"[VIEW_DEBUG] Recebeu notificação: {event_type}") # Para debug
        if event_type == "NOVO_GRUPO_CRIADO":
            df_grupo = data_payload.get("dataframe")
            group_id = data_payload.get("id")
            if df_grupo is not None:
                self.mostrar_dataframe_grupo(df_grupo, f"Novo Grupo {group_id} Criado") # Removido "(via Observer)"
        elif event_type == "GRUPO_PREENCHIDO":
            df_membros = data_payload.get("dataframe")
            group_id = data_payload.get("id")
            if df_membros is not None:
                self.mostrar_dataframe_grupo(df_membros, f"Novos membros adicionados ao Grupo {group_id}") # Removido "(via Observer)"
        elif event_type == "TODOS_ALOCADOS":
            self.confirmar_saida_sem_nao_alocados()
        elif event_type == "NENHUM_NAO_ALOCADO_PARA_PROCESSAR":
             self.exibir_nenhum_aluno_nao_alocado_para_processar()
        elif event_type == "ERRO_ARQUIVO_ALUNOS_NAO_ENCONTRADO":
            self.mostrar_mensagem(f"ERRO CRÍTICO: Arquivo de dados dos alunos não encontrado em {data_payload}. O programa não pode continuar.")
        elif event_type == "ERRO_CARREGAR_ALUNOS":
            self.mostrar_mensagem(f"ERRO CRÍTICO: Não foi possível carregar os dados dos alunos: {data_payload}. O programa não pode continuar.")
        elif event_type == "AVISO_MAPEAMENTO_INDICE_FALHOU":
            self.mostrar_mensagem("Aviso: Dados dos alunos não carregados antes dos grupos. Mapeamento de índice pode ter falhado.")
        elif event_type == "ERRO_CARREGAR_GRUPOS":
             self.mostrar_mensagem(f"Erro ao carregar grupos existentes: {data_payload}")
        elif event_type == "ERRO_SALVAR_GRUPOS":
            self.mostrar_mensagem(f"Erro ao salvar alterações nos grupos: {data_payload}")
        # Adicione mais tratamentos de eventos conforme necessário

    def mostrar_mensagem(self, mensagem):
        print(mensagem)

    def mostrar_dataframe_grupo(self, df_grupo, titulo="Detalhes do Grupo"):
        if df_grupo.empty:
            self.mostrar_mensagem(f"{titulo}: Nenhum aluno para exibir.")
            return
        self.mostrar_mensagem(f"\n--- {titulo} ---")
        print(df_grupo.to_string(index=False))
        self.mostrar_mensagem("------------------------------------")

    def confirmar_saida_sem_nao_alocados(self):
        self.mostrar_mensagem("\nTodos os alunos já estão alocados em grupos.")

    def exibir_erro_carregamento_dados(self): # Pode ser chamado pelo controller ou via update
        self.mostrar_mensagem("ERRO CRÍTICO: Não foi possível carregar os dados dos alunos. O programa não pode continuar.")

    def exibir_nenhum_aluno_nao_alocado_para_processar(self):
        self.mostrar_mensagem("\nNão há alunos não alocados disponíveis para formar novos grupos ou preencher vagas existentes.")