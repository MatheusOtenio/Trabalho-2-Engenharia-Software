# view.py
# Interface via terminal para interação com o usuário

import os
from datetime import datetime

class TerminalView:
    def __init__(self, controller):
        self.controller = controller
    
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Exibe mensagem de boas-vindas"""
        self.clear_screen()
        print("====================================================")
        print("  SISTEMA DE GRUPOS DE ESTUDO COM CHAT EM TERMINAL")
        print("====================================================")
        print("Desenvolvido para a disciplina de Engenharia de Software")
        print("\n")
    
    def show_main_menu(self):
        """Exibe o menu principal"""
        print("\nMENU PRINCIPAL")
        print("1. Criar novo grupo")
        print("2. Listar grupos existentes")
        print("3. Gerenciar grupo")
        print("4. Entrar em um chat de grupo")
        print("0. Sair")
        return input("\nEscolha uma opção: ")
    
    def create_group_menu(self):
        """Menu para criação de grupo"""
        self.clear_screen()
        print("===== CRIAR NOVO GRUPO =====\n")
        
        group_name = input("Nome do grupo: ")
        try:
            max_users = int(input("Número máximo de usuários (padrão: 10): ") or "10")
        except ValueError:
            max_users = 10
            print("Valor inválido. Usando o padrão: 10 usuários.")
        
        success, message = self.controller.create_group(group_name, max_users)
        print(f"\n{message}")
        input("\nPressione ENTER para continuar...")
    
    def list_groups(self):
        """Lista todos os grupos existentes"""
        self.clear_screen()
        print("===== GRUPOS EXISTENTES =====\n")
        
        groups = self.controller.get_all_groups()
        if not groups:
            print("Não há grupos cadastrados.")
        else:
            for i, group in enumerate(groups, 1):
                print(f"{i}. {group.name} ({len(group.members)}/{group.max_users} membros)")
        
        input("\nPressione ENTER para continuar...")
    
    def manage_group_menu(self):
        """Menu para gerenciar um grupo"""
        while True:
            self.clear_screen()
            print("===== GERENCIAR GRUPO =====\n")
            
            groups = self.controller.get_all_groups()
            if not groups:
                print("Não há grupos cadastrados.")
                input("\nPressione ENTER para continuar...")
                return
            
            print("Selecione um grupo:")
            for i, group in enumerate(groups, 1):
                print(f"{i}. {group.name}")
            print("0. Voltar")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                if choice == 0:
                    return
                
                if 1 <= choice <= len(groups):
                    selected_group = groups[choice-1]
                    self.manage_specific_group(selected_group.name)
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
            except ValueError:
                print("\nOpção inválida!")
                input("Pressione ENTER para continuar...")
    
    def manage_specific_group(self, group_name):
        """Menu para gerenciar um grupo específico"""
        while True:
            self.clear_screen()
            group = self.controller.get_group(group_name)
            if not group:
                print(f"Grupo '{group_name}' não encontrado!")
                input("\nPressione ENTER para continuar...")
                return
            
            print(f"===== GERENCIANDO GRUPO: {group.name} =====\n")
            print(f"Membros: {len(group.members)}/{group.max_users}")
            print("\nOpções:")
            print("1. Adicionar usuário")
            print("2. Remover usuário")
            print("3. Listar membros")
            print("4. Excluir grupo")
            print("0. Voltar")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                
                if choice == 0:
                    return
                elif choice == 1:
                    self.add_user_to_group(group_name)
                elif choice == 2:
                    self.remove_user_from_group(group_name)
                elif choice == 3:
                    self.list_group_members(group_name)
                elif choice == 4:
                    if self.confirm_delete_group(group_name):
                        return
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
            except ValueError:
                print("\nOpção inválida!")
                input("Pressione ENTER para continuar...")
    
    def add_user_to_group(self, group_name):
        """Adiciona um usuário ao grupo"""
        self.clear_screen()
        print(f"===== ADICIONAR USUÁRIO AO GRUPO: {group_name} =====\n")
        
        # Listar usuários disponíveis
        all_users = self.controller.data_manager.get_all_users()
        if not all_users:
            print("Não há usuários cadastrados no sistema.")
            input("\nPressione ENTER para continuar...")
            return
        
        print("Usuários disponíveis:")
        for user in all_users:
            print(f"ID: {user.id}, Nome: {user.name}, Email: {user.email}")
        
        user_id = input("\nDigite o ID do usuário que deseja adicionar: ")
        success, message = self.controller.add_user_to_group(group_name, user_id)
        print(f"\n{message}")
        input("\nPressione ENTER para continuar...")
    
    def remove_user_from_group(self, group_name):
        """Remove um usuário do grupo"""
        self.clear_screen()
        print(f"===== REMOVER USUÁRIO DO GRUPO: {group_name} =====\n")
        
        # Listar membros do grupo
        members, error = self.controller.get_group_members(group_name)
        if error:
            print(error)
            input("\nPressione ENTER para continuar...")
            return
        
        if not members:
            print("O grupo não possui membros.")
            input("\nPressione ENTER para continuar...")
            return
        
        print("Membros do grupo:")
        for user in members:
            print(f"ID: {user.id}, Nome: {user.name}, Email: {user.email}")
        
        user_id = input("\nDigite o ID do usuário que deseja remover: ")
        success, message = self.controller.remove_user_from_group(group_name, user_id)
        print(f"\n{message}")
        input("\nPressione ENTER para continuar...")
    
    def list_group_members(self, group_name):
        """Lista os membros de um grupo"""
        self.clear_screen()
        print(f"===== MEMBROS DO GRUPO: {group_name} =====\n")
        
        members, error = self.controller.get_group_members(group_name)
        if error:
            print(error)
        elif not members:
            print("O grupo não possui membros.")
        else:
            for i, user in enumerate(members, 1):
                print(f"{i}. {user.name} ({user.email})")
        
        input("\nPressione ENTER para continuar...")
    
    def confirm_delete_group(self, group_name):
        """Confirma a exclusão de um grupo"""
        self.clear_screen()
        print(f"===== EXCLUIR GRUPO: {group_name} =====\n")
        print("ATENÇÃO: Esta ação não pode ser desfeita!")
        confirm = input("\nDigite o nome do grupo para confirmar a exclusão: ")
        
        if confirm == group_name:
            success, message = self.controller.delete_group(group_name)
            print(f"\n{message}")
            input("\nPressione ENTER para continuar...")
            return True
        else:
            print("\nNome do grupo não corresponde. Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return False
    
    def chat_menu(self):
        """Menu para entrar em um chat de grupo"""
        while True:
            self.clear_screen()
            print("===== CHAT DE GRUPO =====\n")
            
            groups = self.controller.get_all_groups()
            if not groups:
                print("Não há grupos cadastrados.")
                input("\nPressione ENTER para continuar...")
                return
            
            print("Selecione um grupo para entrar no chat:")
            for i, group in enumerate(groups, 1):
                print(f"{i}. {group.name} ({len(group.members)} membros)")
            print("0. Voltar")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                if choice == 0:
                    return
                
                if 1 <= choice <= len(groups):
                    selected_group = groups[choice-1]
                    success, message = self.controller.select_group(selected_group.name)
                    if success:
                        self.enter_chat(selected_group.name)
                    else:
                        print(f"\n{message}")
                        input("\nPressione ENTER para continuar...")
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
            except ValueError:
                print("\nOpção inválida!")
                input("Pressione ENTER para continuar...")
    
    def enter_chat(self, group_name):
        """Interface de chat para um grupo específico"""
        self.clear_screen()
        print(f"===== CHAT DO GRUPO: {group_name} =====\n")
        
        # Exibe mensagens anteriores
        messages, _ = self.controller.get_group_messages(group_name)
        if messages:
            for msg in messages:
                print(f"{msg.sender.name}: {msg.content}")
        
        # Solicita ID do usuário para o chat
        user_id = input("\nDigite seu ID de usuário para entrar no chat: ")
        is_member, error = self.controller.user_in_group(user_id, group_name)
        
        if error:
            print(f"\n{error}")
            input("\nPressione ENTER para continuar...")
            return
        
        if not is_member:
            print("\nVocê não é membro deste grupo. Apenas membros podem participar do chat.")
            input("\nPressione ENTER para continuar...")
            return
        
        # Obtém o usuário e identifica seu tipo (User, Moderator ou Admin)
        user = self.controller.data_manager.get_user_by_id(user_id)
        user_type = self.get_user_type(user)
        
        # Exibe mensagem de boas-vindas com o tipo de usuário
        print(f"\nBem-vindo(a) ao chat, {user.name}! ({user_type})")
        
        # Exibe comandos disponíveis com base no tipo de usuário
        self.show_chat_commands(user_type)
        
        while True:
            message_content = input("\n> ")
            command = message_content.lower()
            
            if command == 'sair':
                break
            elif command == 'usuarios':
                self.show_group_users(group_name)
            elif command == 'limpar':
                self.clear_chat_screen(group_name, user_type)
            elif command == 'moderar' and user_type in ['Moderador', 'Administrador']:
                self.moderation_menu(user, group_name, user_type)
            elif command == 'historico':
                self.show_message_history(group_name)
            elif command == 'comandos':
                self.show_chat_commands(user_type)
            elif message_content.strip():
                success, message = self.controller.send_message(user_id, message_content)
                if not success:
                    print(f"Erro: {message}")
    
    def get_user_type(self, user):
        """Identifica o tipo de usuário (User, Moderator ou Admin)"""
        from user_factory import Admin, Moderator
        
        if isinstance(user, Admin):
            return "Administrador"
        elif isinstance(user, Moderator):
            return "Moderador"
        else:
            return "Usuário"
    
    def show_chat_commands(self, user_type):
        """Exibe os comandos disponíveis com base no tipo de usuário"""
        print("\nComandos disponíveis:")
        print("- 'sair': Voltar ao menu")
        print("- 'usuarios': Ver usuários online")
        print("- 'historico': Ver mensagens recentes")
        print("- 'limpar': Limpar tela")
        print("- 'comandos': Exibir esta lista de comandos")
        
        # Exibe comandos de moderação apenas para Moderadores e Administradores
        if user_type in ['Moderador', 'Administrador']:
            print("- 'moderar': Opções de moderação (Moderador/Administrador)")
    
    def show_group_users(self, group_name):
        """Exibe os usuários do grupo"""
        members, _ = self.controller.get_group_members(group_name)
        print("\nUsuários no grupo:")
        for member in members:
            user_type = self.get_user_type(member)
            print(f"- {member.name} ({user_type})")
    
    def clear_chat_screen(self, group_name, user_type):
        """Limpa a tela do chat e exibe o cabeçalho"""
        self.clear_screen()
        print(f"===== CHAT DO GRUPO: {group_name} =====\n")
        self.show_chat_commands(user_type)
        print("\n--- Conversa ---")
    
    def show_message_history(self, group_name, limit=10):
        """Exibe as últimas mensagens do grupo com numeração"""
        messages, _ = self.controller.get_group_messages(group_name)
        
        if not messages:
            print("\nNão há mensagens no histórico.")
            return []
        
        # Obtém as últimas 'limit' mensagens
        recent_messages = messages[-limit:] if len(messages) > limit else messages
        
        print("\nÚLTIMAS MENSAGENS:")
        for i, msg in enumerate(recent_messages, 1):
            print(f"{i}. {msg.sender.name}: {msg.content}")
        
        return recent_messages
    
    def moderation_menu(self, user, group_name, user_type):
        """Exibe o menu de moderação com opções baseadas no tipo de usuário"""
        group = self.controller.get_group(group_name)
        if not group:
            print("\nGrupo não encontrado!")
            return
        
        while True:
            self.clear_screen()
            print(f"MENU DE MODERAÇÃO ({user_type})")
            print("1. Silenciar usuário")
            print("2. Remover mensagem")
            print("3. Listar usuários do grupo")
            
            # Opções exclusivas para Administradores
            if user_type == "Administrador":
                print("4. Banir usuário (Admin)")
                print("5. Deletar grupo (Admin)")
            
            print("0. Voltar")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                
                if choice == 0:
                    self.clear_chat_screen(group_name, user_type)
                    return
                elif choice == 1:
                    self.mute_user_flow(user, group)
                elif choice == 2:
                    self.remove_message_flow(user, group)
                elif choice == 3:
                    self.list_users_with_permissions(group_name)
                    input("\nPressione ENTER para continuar...")
                elif choice == 4 and user_type == "Administrador":
                    self.ban_user_flow(user, group)
                elif choice == 5 and user_type == "Administrador":
                    if self.delete_group_flow(user, group):
                        return
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
            except ValueError:
                print("\nOpção inválida!")
                input("Pressione ENTER para continuar...")
    
    def mute_user_flow(self, moderator, group):
        """Fluxo para silenciar um usuário"""
        self.clear_screen()
        print(f"===== SILENCIAR USUÁRIO NO GRUPO: {group.name} =====\n")
        
        # Lista os membros do grupo
        members = group.get_members()
        if not members:
            print("O grupo não possui membros.")
            input("\nPressione ENTER para continuar...")
            return
        
        print("Membros do grupo:")
        for i, member in enumerate(members, 1):
            user_type = self.get_user_type(member)
            print(f"{i}. ID: {member.id}, Nome: {member.name} ({user_type})")
        
        # Solicita o ID do usuário a ser silenciado
        user_id = input("\nDigite o ID do usuário que deseja silenciar: ")
        user = self.controller.data_manager.get_user_by_id(user_id)
        
        if not user:
            print(f"\nUsuário com ID '{user_id}' não encontrado.")
            input("\nPressione ENTER para continuar...")
            return
        
        # Solicita a duração do silenciamento
        try:
            duration = int(input("\nDuração do silenciamento em minutos (padrão: 30): ") or "30")
        except ValueError:
            duration = 30
            print("Valor inválido. Usando o padrão: 30 minutos.")
        
        # Confirma a ação
        confirm = input(f"\nConfirmar silenciamento de {user.name} por {duration} minutos? (s/n): ")
        if confirm.lower() != 's':
            print("\nOperação cancelada.")
            input("\nPressione ENTER para continuar...")
            return
        
        # Executa o silenciamento
        success, message = moderator.mute_user(user, group, duration)
        print(f"\n{'✓' if success else '✗'} {message}")
        input("\nPressione ENTER para continuar...")
    
    def remove_message_flow(self, moderator, group):
        """Fluxo para remover uma mensagem"""
        self.clear_screen()
        print(f"===== REMOVER MENSAGEM DO GRUPO: {group.name} =====\n")
        
        # Mostra as últimas mensagens numeradas
        recent_messages = self.show_message_history(group.name)
        if not recent_messages:
            input("\nPressione ENTER para continuar...")
            return
        
        # Solicita o número da mensagem a ser removida
        try:
            msg_num = int(input("\nDigite o número da mensagem a remover (0 para cancelar): "))
            if msg_num == 0:
                print("\nOperação cancelada.")
                input("\nPressione ENTER para continuar...")
                return
            
            if 1 <= msg_num <= len(recent_messages):
                message = recent_messages[msg_num-1]
                
                # Confirma a remoção
                confirm = input(f"\nConfirmar remoção da mensagem \"{message.sender.name}: {message.content}\"? (s/n): ")
                if confirm.lower() != 's':
                    print("\nOperação cancelada.")
                    input("\nPressione ENTER para continuar...")
                    return
                
                # Executa a remoção
                success, result_msg = moderator.remove_message(message, group)
                print(f"\n{'✓' if success else '✗'} {result_msg}")
            else:
                print("\nNúmero de mensagem inválido.")
        except ValueError:
            print("\nEntrada inválida. Digite um número.")
        
        input("\nPressione ENTER para continuar...")
    
    def list_users_with_permissions(self, group_name):
        """Lista os usuários do grupo com suas permissões"""
        self.clear_screen()
        print(f"===== USUÁRIOS DO GRUPO: {group_name} =====\n")
        
        members, error = self.controller.get_group_members(group_name)
        if error:
            print(error)
            return
        
        if not members:
            print("O grupo não possui membros.")
            return
        
        print("Lista de membros e suas permissões:")
        for i, member in enumerate(members, 1):
            user_type = self.get_user_type(member)
            print(f"{i}. {member.name} ({member.email}) - {user_type}")
    
    def ban_user_flow(self, admin, group):
        """Fluxo para banir um usuário permanentemente (apenas Admin)"""
        self.clear_screen()
        print(f"===== BANIR USUÁRIO DO GRUPO: {group.name} =====\n")
        print("ATENÇÃO: Esta ação é permanente e não pode ser desfeita!")
        
        # Lista os membros do grupo
        members = group.get_members()
        if not members:
            print("O grupo não possui membros.")
            input("\nPressione ENTER para continuar...")
            return
        
        print("\nMembros do grupo:")
        for i, member in enumerate(members, 1):
            user_type = self.get_user_type(member)
            print(f"{i}. ID: {member.id}, Nome: {member.name} ({user_type})")
        
        # Solicita o ID do usuário a ser banido
        user_id = input("\nDigite o ID do usuário que deseja banir: ")
        user = self.controller.data_manager.get_user_by_id(user_id)
        
        if not user:
            print(f"\nUsuário com ID '{user_id}' não encontrado.")
            input("\nPressione ENTER para continuar...")
            return
        
        # Confirma o banimento
        confirm = input(f"\nConfirmar banimento PERMANENTE de {user.name} do grupo {group.name}? (digite 'confirmar' para prosseguir): ")
        if confirm.lower() != 'confirmar':
            print("\nOperação cancelada.")
            input("\nPressione ENTER para continuar...")
            return
        
        # Executa o banimento
        success, message = admin.ban_user(user, group)
        print(f"\n{'✓' if success else '✗'} {message}")
        input("\nPressione ENTER para continuar...")
    
    def delete_group_flow(self, admin, group):
        """Fluxo para deletar um grupo (apenas Admin)"""
        self.clear_screen()
        print(f"===== DELETAR GRUPO: {group.name} =====\n")
        print("ATENÇÃO: Esta ação não pode ser desfeita e removerá PERMANENTEMENTE o grupo e todo seu histórico!")
        
        # Primeira confirmação
        confirm1 = input("\nDigite o nome do grupo para confirmar a exclusão: ")
        if confirm1 != group.name:
            print("\nNome do grupo não corresponde. Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return False
        
        # Segunda confirmação
        confirm2 = input("\nTem certeza? Digite 'confirmar exclusão' para prosseguir: ")
        if confirm2.lower() != 'confirmar exclusão':
            print("\nOperação cancelada.")
            input("\nPressione ENTER para continuar...")
            return False
        
        # Executa a exclusão do grupo
        success, message = admin.delete_group(group, self.controller)
        print(f"\n{'✓' if success else '✗'} {message}")
        input("\nPressione ENTER para continuar...")
        return success
    
    def run(self):
        """Executa o loop principal da aplicação"""
        self.show_welcome()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == '0':
                self.clear_screen()
                print("Obrigado por usar o Sistema de Grupos de Estudo!")
                print("Encerrando...")
                break
            elif choice == '1':
                self.create_group_menu()
            elif choice == '2':
                self.list_groups()
            elif choice == '3':
                self.manage_group_menu()
            elif choice == '4':
                self.chat_menu()
            else:
                print("\nOpção inválida! Por favor, tente novamente.")
                input("Pressione ENTER para continuar...")