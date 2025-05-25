import subprocess
import os

def menu():
    print("\n===== SISTEMA DE GRUPOS DE ESTUDO =====\n")
    print("Escolha um projeto para executar:")
    print("1 - Projeto do Caio (Gerenciamento de Perfis e Grupos)")
    print("2 - Projeto do João (Sistema de Grupos)")
    print("3 - Projeto do Matheus (Chat de Grupos de Estudo)")
    print("4 - Projeto do Viana (Montagem de Grupos)")
    print("0 - Sair")
    return input("\nOpção: ")

def clear_screen():
    # Limpa a tela do console (funciona em Windows)
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        opcao = menu()
        
        try:
            if opcao == "1":
                print("\nExecutando o projeto do Caio...\n")
                subprocess.run(["python", "caio/main.py"])
                input("\nPressione Enter para voltar ao menu principal...")
            elif opcao == "2":
                print("\nExecutando o projeto do João...\n")
                subprocess.run(["python", "jao/main.py"])
                input("\nPressione Enter para voltar ao menu principal...")
            elif opcao == "3":
                print("\nExecutando o projeto do Matheus...\n")
                subprocess.run(["python", "matheus/main.py"])
                input("\nPressione Enter para voltar ao menu principal...")
            elif opcao == "4":
                print("\nExecutando o projeto do Viana...\n")
                subprocess.run(["python", "viana/main.py"])
                input("\nPressione Enter para voltar ao menu principal...")
            elif opcao == "0":
                print("\nSaindo do sistema. Até logo!")
                break
            else:
                print("\nOpção inválida, tente novamente!")
                input("\nPressione Enter para continuar...")
        except Exception as e:
            print(f"\nErro ao executar o projeto: {e}")
            input("\nPressione Enter para voltar ao menu principal...")

if __name__ == "__main__":
    main()