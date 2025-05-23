# data.py
# Responsável pela leitura e validação dos dados de usuários do arquivo CSV

import csv
from models import User
from user_factory import UserFactory

class DataManager:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.users = []
        self.load_users()
    
    def load_users(self):
        """Carrega os usuários do arquivo CSV usando a UserFactory"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                # Pula o cabeçalho se existir
                header = next(csv_reader, None)
                
                # Determina os índices das colunas
                id_idx, name_idx, email_idx = 0, 1, 2
                type_idx = 3 if len(header) > 3 else None  # Verifica se existe coluna de tipo
                
                for row in csv_reader:
                    if len(row) >= 3:  # Verifica se a linha tem dados suficientes
                        user_id = row[id_idx]
                        name = row[name_idx]
                        email = row[email_idx]
                        
                        # Obtém o tipo de usuário se disponível
                        user_type = row[type_idx] if type_idx is not None and len(row) > type_idx else "user"
                        
                        # Cria um novo usuário usando a factory e adiciona à lista
                        user = UserFactory.create_user(user_type, user_id, name, email)
                        self.users.append(user)
            return True, f"Carregados {len(self.users)} usuários com sucesso"
        except FileNotFoundError:
            return False, f"Arquivo {self.csv_file_path} não encontrado"
        except Exception as e:
            return False, f"Erro ao carregar usuários: {str(e)}"
    
    def get_all_users(self):
        """Retorna todos os usuários carregados"""
        return self.users
    
    def get_user_by_id(self, user_id):
        """Busca um usuário pelo ID"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_user_by_name(self, name):
        """Busca um usuário pelo nome (pode retornar múltiplos usuários)"""
        matching_users = [user for user in self.users if user.name.lower() == name.lower()]
        return matching_users
    
    def get_user_by_email(self, email):
        """Busca um usuário pelo email"""
        for user in self.users:
            if user.email.lower() == email.lower():
                return user
        return None
    
    def create_sample_csv(self):
        """Cria um arquivo CSV de exemplo com alguns usuários e seus tipos"""
        try:
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                # Escreve o cabeçalho com a coluna de tipo
                csv_writer.writerow(['id', 'nome', 'email', 'tipo'])
                # Escreve alguns usuários de exemplo com seus tipos
                csv_writer.writerow(['1', 'João Silva', 'joao@exemplo.com', 'admin'])
                csv_writer.writerow(['2', 'Maria Santos', 'maria@exemplo.com', 'moderator'])
                csv_writer.writerow(['3', 'Pedro Oliveira', 'pedro@exemplo.com', 'user'])
                csv_writer.writerow(['4', 'Ana Souza', 'ana@exemplo.com', 'moderator'])
                csv_writer.writerow(['5', 'Carlos Ferreira', 'carlos@exemplo.com', 'user'])
            return True, f"Arquivo CSV de exemplo criado em {self.csv_file_path}"
        except Exception as e:
            return False, f"Erro ao criar arquivo CSV de exemplo: {str(e)}"