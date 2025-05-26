import matplotlib.pyplot as plt
import numpy as np
from sistema_controller import SistemaController

class Dashboard:
    def __init__(self):
        self.sistema = SistemaController.get_instance()
    
    def gerar_grafico_materias_populares(self):
        """Gera um gráfico de barras das matérias mais populares"""
        # Contagem de matérias
        contagem_materias = {}
        for usuario in self.sistema.usuarios:
            for materia in usuario.materias_interesse:
                if materia in contagem_materias:
                    contagem_materias[materia] += 1
                else:
                    contagem_materias[materia] = 1
        
        # Ordenar por popularidade
        materias_ordenadas = sorted(contagem_materias.items(), key=lambda x: x[1], reverse=True)
        
        # Limitar a 10 matérias para melhor visualização
        materias = [m[0] for m in materias_ordenadas[:10]]
        contagens = [m[1] for m in materias_ordenadas[:10]]
        
        # Criar gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(materias, contagens, color='skyblue')
        plt.xlabel('Matérias')
        plt.ylabel('Número de Estudantes')
        plt.title('Matérias Mais Populares')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Salvar o gráfico
        plt.savefig('materias_populares.png')
        print("\n✅ Gráfico de matérias populares gerado com sucesso!")
        plt.close()
    
    def gerar_grafico_distribuicao_grupos(self):
        """Gera um gráfico de pizza da distribuição de grupos"""
        # Contagem de grupos por matéria
        if not self.sistema.grupos:
            print("\n❌ Não há grupos para gerar o gráfico de distribuição.")
            return
            
        materias = list(self.sistema.grupos.keys())
        membros = [len(self.sistema.grupos[m].membros) for m in materias]
        
        # Criar gráfico
        plt.figure(figsize=(10, 8))
        plt.pie(membros, labels=materias, autopct='%1.1f%%', startangle=140, shadow=True)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Distribuição de Membros por Grupo')
        plt.tight_layout()
        
        # Salvar o gráfico
        plt.savefig('distribuicao_grupos.png')
        print("\n✅ Gráfico de distribuição de grupos gerado com sucesso!")
        plt.close()
    
    def gerar_grafico_atividade_usuarios(self):
        """Gera um gráfico de barras da atividade dos usuários (baseado em grupos participados)"""
        usuarios = [u.nome for u in self.sistema.usuarios]
        grupos_participados = [u.grupos_participados for u in self.sistema.usuarios]
        
        # Ordenar por atividade
        dados_ordenados = sorted(zip(usuarios, grupos_participados), key=lambda x: x[1], reverse=True)
        usuarios = [d[0] for d in dados_ordenados]
        grupos_participados = [d[1] for d in dados_ordenados]
        
        # Limitar a 10 usuários para melhor visualização
        usuarios = usuarios[:10]
        grupos_participados = grupos_participados[:10]
        
        # Criar gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(usuarios, grupos_participados, color='lightgreen')
        plt.xlabel('Usuários')
        plt.ylabel('Grupos Participados')
        plt.title('Usuários Mais Ativos (por Grupos Participados)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Salvar o gráfico
        plt.savefig('atividade_usuarios.png')
        print("\n✅ Gráfico de atividade de usuários gerado com sucesso!")
        plt.close()
    
    def mostrar_estatisticas_gerais(self):
        """Mostra estatísticas gerais do sistema"""
        total_usuarios = len(self.sistema.usuarios)
        total_grupos = len(self.sistema.grupos)
        
        # Calcular média de grupos por usuário
        media_grupos = sum(u.grupos_participados for u in self.sistema.usuarios) / total_usuarios if total_usuarios > 0 else 0
        
        # Calcular total de matérias únicas
        materias_unicas = set()
        for u in self.sistema.usuarios:
            materias_unicas.update(u.materias_interesse)
        
        print("\n📊 ESTATÍSTICAS GERAIS DO SISTEMA")
        print(f"👥 Total de usuários: {total_usuarios}")
        print(f"🧩 Total de grupos: {total_grupos}")
        print(f"📘 Total de matérias únicas: {len(materias_unicas)}")
        print(f"📊 Média de grupos por usuário: {media_grupos:.2f}")
        print("-" * 40)
    
    def gerar_dashboard_completo(self):
        """Gera todos os gráficos e estatísticas"""
        print("\n🔄 Gerando dashboard completo...")
        self.mostrar_estatisticas_gerais()
        self.gerar_grafico_materias_populares()
        self.gerar_grafico_distribuicao_grupos()
        self.gerar_grafico_atividade_usuarios()
        print("\n✅ Dashboard completo gerado com sucesso!")