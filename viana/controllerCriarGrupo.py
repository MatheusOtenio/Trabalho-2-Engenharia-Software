# controller.py
from modelCriarGrupo import GerenciadorDados
from visionCriarGrupo import Visao
import pandas as pd

class Controlador:
    def __init__(self, config):
        self.config = config
        self.modelo = GerenciadorDados(config)
        self.visao = Visao()
        
        # Registra a Visao como um observer do Modelo
        self.modelo.register_observer(self.visao)

    def executar_montagem_de_grupo(self):
        self.visao.mostrar_mensagem("Iniciando processo de montagem de grupos...")

        if not self.modelo.carregar_dados_alunos():
            # A notificação de erro já pode ter sido enviada pelo model à view
            return

        self.modelo.precalcular_pares_similaridade()
        if not self.modelo.pares_similaridade:
            self.visao.mostrar_mensagem("Aviso: Não foi possível calcular as similaridades entre os alunos.")

        self.modelo.inicializar_arquivo_grupos()
        grupos_existentes_mapa = self.modelo.carregar_grupos_existentes()

        alunos_nao_alocados_indices = self.modelo.identificar_alunos_nao_alocados(grupos_existentes_mapa)

        if not alunos_nao_alocados_indices:
            # O Model pode notificar a View diretamente sobre isso
            self.modelo._notify_observers("TODOS_ALOCADOS")
            # self.visao.confirmar_saida_sem_nao_alocados() # Removido pois o model notifica
            return

        self.visao.mostrar_mensagem(f"Alunos não alocados encontrados: {len(alunos_nao_alocados_indices)}")
        ids_grupos_com_vagas = self.modelo.encontrar_grupos_com_vagas(grupos_existentes_mapa)

        operacao_realizada = False
        if ids_grupos_com_vagas:
            id_grupo_alvo = ids_grupos_com_vagas[0]
            indices_membros_existentes_no_grupo_alvo = grupos_existentes_mapa.get(id_grupo_alvo, [])
            
            self.visao.mostrar_mensagem(f"\nTentando preencher vagas no grupo {id_grupo_alvo}...")
            
            # O método do modelo agora salva e notifica internamente
            df_novos_membros_adicionados = self.modelo.preencher_grupo_existente(
                id_grupo_alvo,
                indices_membros_existentes_no_grupo_alvo,
                alunos_nao_alocados_indices
            )

            if not df_novos_membros_adicionados.empty:
                operacao_realizada = True
                # A View será atualizada via Observer
                # self.visao.mostrar_dataframe_grupo(df_novos_membros_adicionados, f"Novos membros adicionados ao Grupo {id_grupo_alvo}")
            else:
                self.visao.mostrar_mensagem(f"Não foram adicionados novos membros ao grupo {id_grupo_alvo} (sem candidatos adequados ou vagas).")
        
        elif alunos_nao_alocados_indices: # Só cria novo grupo se ainda houver não alocados
            self.visao.mostrar_mensagem("\nNão há grupos com vagas. Tentando criar um novo grupo...")
            
            proximo_id_grupo = 1
            if grupos_existentes_mapa:
                proximo_id_grupo = max(grupos_existentes_mapa.keys(), default=0) + 1
            
            aluno_base_para_novo_grupo_idx = next(iter(alunos_nao_alocados_indices))
            
            # O método do modelo agora salva e notifica internamente
            df_novo_grupo_criado = self.modelo.criar_novo_grupo(
                aluno_base_para_novo_grupo_idx,
                alunos_nao_alocados_indices,
                proximo_id_grupo
            )

            if not df_novo_grupo_criado.empty:
                operacao_realizada = True
                # A View será atualizada via Observer
                # self.visao.mostrar_dataframe_grupo(df_novo_grupo_criado, f"Novo Grupo {proximo_id_grupo} Criado")
            else:
                self.visao.mostrar_mensagem("Não foi possível criar um novo grupo.")
        
        if not operacao_realizada and not alunos_nao_alocados_indices:
            # Caso onde todos foram alocados na tentativa de preenchimento e não sobrou ninguém para criar novo grupo
             self.modelo._notify_observers("TODOS_ALOCADOS")
        elif not operacao_realizada and alunos_nao_alocados_indices:
            # Caso onde não foi possível nem preencher nem criar, mas ainda há não alocados
            # (pode ser que não haja candidatos para o grupo específico ou para formar um novo sozinho)
            self.modelo._notify_observers("NENHUM_NAO_ALOCADO_PARA_PROCESSAR")


        self.visao.mostrar_mensagem("\nProcesso de montagem de grupo concluído.")