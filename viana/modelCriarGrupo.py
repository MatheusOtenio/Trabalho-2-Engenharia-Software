# model.py
import pandas as pd
from itertools import combinations
import csv
import os

class GerenciadorDados:
    def __init__(self, config):
        self.config = config
        self.df_alunos = None
        self.df_grupos = None
        self.pares_similaridade = {}
        self._observers = []

    def register_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def _notify_observers(self, event_type, data_payload=None):
        for observer in self._observers:
            observer.update(event_type, data_payload)

    def carregar_dados_alunos(self):
        try:
            with open(self.config['DADOS_PATH'], 'r', encoding='latin1') as f:
                sample = f.read(2048)
                try:
                    dialect = csv.Sniffer().sniff(sample, delimiters=';,')
                    sep = dialect.delimiter
                except csv.Error:
                    print("Aviso: Não foi possível detectar o delimitador automaticamente. Usando ';' como padrão.")
                    sep = ';'
            
            self.df_alunos = pd.read_csv(self.config['DADOS_PATH'], sep=sep, encoding='latin1')
            self.df_alunos.columns = self.df_alunos.columns.str.strip().str.lower()
            
            # **** NOVO: Strip whitespace from student names ****
            if 'nome' in self.df_alunos.columns:
                self.df_alunos['nome'] = self.df_alunos['nome'].str.strip()
            
            self.df_alunos['disciplinas'] = self.df_alunos['disciplinas'].apply(
                lambda x: [d.strip() for delim in [';', ','] for d in str(x).split(delim) if d.strip()] if pd.notna(x) else []
            )
            self.df_alunos['periodo'] = pd.to_numeric(self.df_alunos['periodo'], errors='coerce').fillna(0).astype(int)
            print("[MODEL_DEBUG] df_alunos carregado. Nomes stripados. Total de alunos:", len(self.df_alunos))
            return True
        except FileNotFoundError:
            self._notify_observers("ERRO_ARQUIVO_ALUNOS_NAO_ENCONTRADO", self.config['DADOS_PATH'])
            return False
        except Exception as e:
            self._notify_observers("ERRO_CARREGAR_ALUNOS", str(e))
            return False

    def calcular_similaridade_aluno(self, aluno_a_idx, aluno_b_idx):
        # (código existente sem alterações)
        if self.df_alunos is None:
            return 0
        aluno_a = self.df_alunos.loc[aluno_a_idx]
        aluno_b = self.df_alunos.loc[aluno_b_idx]
        score = 0
        if aluno_a['curso'] == aluno_b['curso']:
            score += self.config['PESO_CURSO']
        max_diff_periodo = max(self.df_alunos['periodo'].max() - self.df_alunos['periodo'].min(), 1)
        diff_periodo = abs(aluno_a['periodo'] - aluno_b['periodo'])
        score += self.config['PESO_PERIODO'] * (1 - diff_periodo / max_diff_periodo)
        disciplinas_a = set(aluno_a['disciplinas'])
        disciplinas_b = set(aluno_b['disciplinas'])
        common_disciplinas = len(disciplinas_a.intersection(disciplinas_b))
        max_common_disciplinas = max(len(disciplinas_a), len(disciplinas_b), 1)
        score += self.config['PESO_DISCIPLINA'] * (common_disciplinas / max_common_disciplinas)
        return score


    def precalcular_pares_similaridade(self):
        # (código existente sem alterações)
        if self.df_alunos is None:
            return
        indices_alunos = self.df_alunos.index.tolist()
        self.pares_similaridade = {
            (i, j): self.calcular_similaridade_aluno(i, j)
            for i, j in combinations(indices_alunos, 2)
        }

    def carregar_grupos_existentes(self):
        if not os.path.exists(self.config['GRUPOS_PATH']) or os.path.getsize(self.config['GRUPOS_PATH']) == 0:
            self.inicializar_arquivo_grupos()
            self.df_grupos = pd.DataFrame(columns=['nome', 'curso', 'periodo', 'grupo', 'idx'])
            print("[MODEL_DEBUG] Arquivo de grupos não existia ou estava vazio, inicializado.")
            return {}
        try:
            self.df_grupos = pd.read_csv(self.config['GRUPOS_PATH'], sep=';', encoding='utf-8')
            print(f"[MODEL_DEBUG] df_grupos carregado de CSV (antes do strip e map):\n{self.df_grupos.head()}")

            # **** NOVO: Strip whitespace from names in df_grupos as well ****
            if 'nome' in self.df_grupos.columns:
                self.df_grupos['nome'] = self.df_grupos['nome'].str.strip()

            if self.df_alunos is None:
                self._notify_observers("AVISO_MAPEAMENTO_INDICE_FALHOU", None)
                self.df_grupos['idx'] = -1
                print("[MODEL_DEBUG] df_alunos é None durante carregamento de grupos.")
            else:
                mapa_nome_idx = pd.Series(self.df_alunos.index, index=self.df_alunos['nome']).to_dict()
                self.df_grupos['idx'] = self.df_grupos['nome'].map(mapa_nome_idx).fillna(-1).astype(int)
                print(f"[MODEL_DEBUG] df_grupos APÓS mapeamento de 'idx':\n{self.df_grupos[['nome', 'grupo', 'idx']].head()}")
            
            # **** IMPORTANTE: Considerar apenas mapeamentos válidos ****
            valid_grupos_df = self.df_grupos[self.df_grupos['idx'] != -1]
            
            if len(valid_grupos_df) < len(self.df_grupos):
                print(f"[MODEL_DEBUG] Alunos de grupos.csv não encontrados em Estudantes.csv (idx -1): {len(self.df_grupos) - len(valid_grupos_df)} de {len(self.df_grupos)}")
                print(f"Detalhes dos não mapeados:\n{self.df_grupos[self.df_grupos['idx'] == -1][['nome','grupo']]}")

            grupos_com_indices = valid_grupos_df.groupby('grupo')['idx'].apply(list).to_dict()
            print(f"[MODEL_DEBUG] grupos_com_indices FORMADO (apenas com idx válidos): {grupos_com_indices}")
            return grupos_com_indices
        except pd.errors.EmptyDataError: # Tratado pelo check de os.path.getsize no início
            self.inicializar_arquivo_grupos() 
            self.df_grupos = pd.DataFrame(columns=['nome', 'curso', 'periodo', 'grupo', 'idx'])
            print("[MODEL_DEBUG] Arquivo de grupos resultou em EmptyDataError, re-inicializado.")
            return {}
        except Exception as e:
            self._notify_observers("ERRO_CARREGAR_GRUPOS", str(e))
            self.df_grupos = pd.DataFrame(columns=['nome', 'curso', 'periodo', 'grupo', 'idx'])
            print(f"[MODEL_DEBUG] Exceção ao carregar grupos: {e}")
            return {}
            
    def inicializar_arquivo_grupos(self):
        # (código existente sem alterações)
        if not os.path.exists(self.config['GRUPOS_PATH']) or os.path.getsize(self.config['GRUPOS_PATH']) == 0:
            with open(self.config['GRUPOS_PATH'], 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['nome', 'curso', 'periodo', 'grupo'])

    def salvar_novos_membros_grupo(self, df_novos_membros):
        # (código existente sem alterações)
        try:
            self.inicializar_arquivo_grupos()
            colunas_para_salvar = ['nome', 'curso', 'periodo', 'grupo']
            df_para_salvar = df_novos_membros[colunas_para_salvar]

            df_para_salvar.to_csv(
                self.config['GRUPOS_PATH'], sep=';', index=False, encoding='utf-8', mode='a',
                header=not os.path.exists(self.config['GRUPOS_PATH']) or os.path.getsize(self.config['GRUPOS_PATH']) == 0
            )
        except Exception as e:
            self._notify_observers("ERRO_SALVAR_GRUPOS", str(e))


    def identificar_alunos_nao_alocados(self, grupos_existentes_indices):
        if self.df_alunos is None:
            print("[MODEL_DEBUG] df_alunos é None em identificar_alunos_nao_alocados.")
            return set()
        todos_indices_alunos = set(self.df_alunos.index.tolist())
        indices_alocados = set()
        for indices_no_grupo in grupos_existentes_indices.values():
            indices_alocados.update(indices_no_grupo)
        
        print(f"[MODEL_DEBUG] Total de alunos (df_alunos): {len(todos_indices_alunos)}")
        print(f"[MODEL_DEBUG] Índices alocados (de grupos_existentes_indices): {len(indices_alocados)}")
        # print(f"DEBUG: indices_alocados: {indices_alocados}") # Descomente para ver os índices
        alunos_nao_alocados = todos_indices_alunos - indices_alocados
        print(f"[MODEL_DEBUG] Alunos não alocados calculados: {len(alunos_nao_alocados)}")
        return alunos_nao_alocados

    def encontrar_grupos_com_vagas(self, grupos_existentes_indices):
        # (código existente sem alterações)
        return [
            gid for gid, idxs in grupos_existentes_indices.items()
            if len(idxs) < self.config['MAX_GRUPO']
        ]

    def criar_novo_grupo(self, base_aluno_idx, alunos_nao_alocados_indices, proximo_group_id):
        # (código existente com pequenas modificações para notificação)
        if self.df_alunos is None:
            return pd.DataFrame()

        copia_alunos_nao_alocados = alunos_nao_alocados_indices.copy()
        # Verifica se base_aluno_idx está na cópia antes de remover
        if base_aluno_idx not in copia_alunos_nao_alocados:
            print(f"[MODEL_DEBUG] ERRO: base_aluno_idx {base_aluno_idx} não encontrado em alunos_nao_alocados_indices para criar_novo_grupo.")
            return pd.DataFrame()
        copia_alunos_nao_alocados.remove(base_aluno_idx) 

        scores_similaridade = []
        for outro_idx in copia_alunos_nao_alocados:
            par_ordenado = tuple(sorted((base_aluno_idx, outro_idx)))
            score = self.pares_similaridade.get(par_ordenado, 0)
            scores_similaridade.append((score, outro_idx))
        
        scores_similaridade.sort(key=lambda x: x[0], reverse=True)

        membros_grupo_indices = [base_aluno_idx]
        for _, idx_candidato in scores_similaridade:
            if len(membros_grupo_indices) < self.config['MAX_GRUPO']:
                membros_grupo_indices.append(idx_candidato)
            else:
                break
        
        # Atualiza o SET original de alunos_nao_alocados_indices
        for idx_membro in membros_grupo_indices:
            alunos_nao_alocados_indices.discard(idx_membro) # Remove do set original

        df_novo_grupo = self.df_alunos.loc[membros_grupo_indices, ['nome', 'curso', 'periodo']].copy()
        df_novo_grupo['grupo'] = proximo_group_id
        
        if not df_novo_grupo.empty:
            self.salvar_novos_membros_grupo(df_novo_grupo)
            self._notify_observers("NOVO_GRUPO_CRIADO", {"dataframe": df_novo_grupo, "id": proximo_group_id})
        return df_novo_grupo

    def preencher_grupo_existente(self, group_id_alvo, indices_membros_existentes, alunos_nao_alocados_indices):
        # (código existente com pequenas modificações para notificação)
        if self.df_alunos is None or not alunos_nao_alocados_indices:
            return pd.DataFrame()

        vagas_disponiveis = self.config['MAX_GRUPO'] - len(indices_membros_existentes)
        if vagas_disponiveis <= 0:
            return pd.DataFrame()

        aluno_base_idx = indices_membros_existentes[0]
        scores_similaridade = []
        for idx_candidato in alunos_nao_alocados_indices:
            if idx_candidato not in indices_membros_existentes:
                par_ordenado = tuple(sorted((aluno_base_idx, idx_candidato)))
                score = self.pares_similaridade.get(par_ordenado, 0)
                scores_similaridade.append((score, idx_candidato))
        
        scores_similaridade.sort(key=lambda x: x[0], reverse=True)
        novos_membros_adicionados_indices = []
        for _, idx_candidato in scores_similaridade:
            if len(novos_membros_adicionados_indices) < vagas_disponiveis:
                novos_membros_adicionados_indices.append(idx_candidato)
            else:
                break
        
        # Atualiza o SET original de alunos_nao_alocados_indices
        for idx_adicionado in novos_membros_adicionados_indices:
            alunos_nao_alocados_indices.discard(idx_adicionado) # Remove do set original

        if not novos_membros_adicionados_indices:
            return pd.DataFrame()

        df_novos_membros = self.df_alunos.loc[novos_membros_adicionados_indices, ['nome', 'curso', 'periodo']].copy()
        df_novos_membros['grupo'] = group_id_alvo
        
        if not df_novos_membros.empty:
            self.salvar_novos_membros_grupo(df_novos_membros)
            self._notify_observers("GRUPO_PREENCHIDO", {"dataframe": df_novos_membros, "id": group_id_alvo})
        return df_novos_membros