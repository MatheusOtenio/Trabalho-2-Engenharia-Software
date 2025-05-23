# user_factory.py
# Implementa o Factory Method Pattern para criar diferentes tipos de usuários

from models import User

class Moderator(User):
    """Classe para usuários com permissões de moderação.
    
    Herda de User e adiciona funcionalidades específicas para moderadores.
    
    Attributes:
        id (str): Identificador único do usuário
        name (str): Nome do usuário
        email (str): Email do usuário
    """
    
    def __init__(self, id, name, email):
        super().__init__(id, name, email)
    
    def remove_message(self, message, group):
        """Remove uma mensagem de um grupo.
        
        Args:
            message (Message): A mensagem a ser removida
            group (Group): O grupo do qual a mensagem será removida
            
        Returns:
            tuple: (bool, str) indicando sucesso/falha e mensagem
        """
        if message in group.messages:
            group.messages.remove(message)
            return True, f"Mensagem removida por {self.name}"
        return False, "Mensagem não encontrada"
    
    def mute_user(self, user, group, duration=30):
        """Silencia temporariamente um usuário em um grupo.
        
        Args:
            user (User): O usuário a ser silenciado
            group (Group): O grupo onde o usuário será silenciado
            duration (int): Duração do silenciamento em minutos
            
        Returns:
            tuple: (bool, str) indicando sucesso/falha e mensagem
        """
        if user in group.members:
            # Aqui poderia ser implementada a lógica de silenciamento
            # Por simplicidade, apenas retornamos uma mensagem de sucesso
            return True, f"Usuário {user.name} silenciado por {duration} minutos"
        return False, "Usuário não é membro do grupo"


class Admin(Moderator):
    """Classe para usuários com permissões administrativas.
    
    Herda de Moderator e adiciona funcionalidades específicas para administradores.
    
    Attributes:
        id (str): Identificador único do usuário
        name (str): Nome do usuário
        email (str): Email do usuário
    """
    
    def __init__(self, id, name, email):
        super().__init__(id, name, email)
    
    def delete_group(self, group, controller):
        """Deleta um grupo do sistema.
        
        Args:
            group (Group): O grupo a ser deletado
            controller (GroupController): O controlador que gerencia os grupos
            
        Returns:
            tuple: (bool, str) indicando sucesso/falha e mensagem
        """
        return controller.delete_group(group.name)
    
    def ban_user(self, user, group):
        """Bane permanentemente um usuário de um grupo.
        
        Args:
            user (User): O usuário a ser banido
            group (Group): O grupo do qual o usuário será banido
            
        Returns:
            tuple: (bool, str) indicando sucesso/falha e mensagem
        """
        if user in group.members:
            group.members.remove(user)
            return True, f"Usuário {user.name} banido permanentemente do grupo {group.name}"
        return False, "Usuário não é membro do grupo"


class UserFactory:
    """Factory Method para criar diferentes tipos de usuários.
    
    Esta classe implementa o padrão Factory Method para criar instâncias
    de User, Moderator ou Admin com base no tipo especificado.
    """
    
    @staticmethod
    def create_user(user_type, id, name, email):
        """Cria um usuário do tipo especificado.
        
        Args:
            user_type (str): O tipo de usuário a ser criado ('user', 'moderator', 'admin')
            id (str): Identificador único do usuário
            name (str): Nome do usuário
            email (str): Email do usuário
            
        Returns:
            User: Uma instância de User, Moderator ou Admin
            
        Raises:
            ValueError: Se os campos obrigatórios estiverem vazios
        """
        # Validação de campos obrigatórios
        if not id or not name or not email:
            raise ValueError("ID, nome e email são campos obrigatórios")
        
        # Criação do usuário com base no tipo
        user_type = user_type.lower() if user_type else "user"
        
        if user_type == "admin":
            return Admin(id, name, email)
        elif user_type == "moderator":
            return Moderator(id, name, email)
        else:
            # Se o tipo for inválido ou 'user', cria um usuário padrão
            if user_type not in ["user", "", None]:
                print(f"Aviso: Tipo de usuário '{user_type}' inválido. Criando usuário padrão.")
            return User(id, name, email)