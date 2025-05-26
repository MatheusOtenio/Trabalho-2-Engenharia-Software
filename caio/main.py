from sistema_controller import SistemaController
from perfil import Perfil
from interface import mostrar_dashboard
from dashboard import Dashboard

def menu():
    sistema = SistemaController.get_instance()

    ra = input("Digite seu RA: ").strip()
    usuario = sistema.buscar_usuario(ra)

    if not usuario:
        nome = input("RA não encontrado. Digite seu nome: ")
        email = input("Digite seu email institucional: ")
        usuario = Perfil(nome, ra, email)
        sistema.adicionar_usuario(usuario)
        print("✅ Usuário criado com sucesso!")
    else:
        print(f"👋 Bem-vindo de volta, {usuario.nome}!")

    mostrar_dashboard(usuario)

    while True:
        print("\n📋 MENU")
        print("1. Alterar nome")
        print("2. Alterar email")
        print("3. Adicionar matéria de interesse")
        print("4. Visualizar dashboard completo")
        print("0. Sair")

        op = input("Escolha uma opção: ").strip()

        if op == "1":
            usuario.nome = input("Novo nome: ")
        elif op == "2":
            usuario.email = input("Novo email: ")
        elif op == "3":
            materia = input("Nome da matéria: ")
            usuario.adicionar_materia(materia)
            sistema.adicionar_usuario_ao_grupo(usuario, materia)
        elif op == "4":
            dashboard = Dashboard()
            dashboard.gerar_dashboard_completo()
        elif op == "0":
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida.")

        sistema.salvar_usuarios()

if __name__ == "__main__":
    menu()
