import os
import platform

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def pause():
    input(f"{Colors.OKBLUE}\nPressione Enter para continuar...{Colors.ENDC}")

def show_menu():
    border = Colors.OKBLUE + '=' * 50 + Colors.ENDC
    print(border)
    title = ' Fórum de Perguntas e Respostas '
    print(Colors.BOLD + Colors.OKCYAN + title.center(50, '=') + Colors.ENDC)
    print(border)
    print(f"{Colors.OKGREEN}[1]{Colors.ENDC} Fazer pergunta")
    print(f"{Colors.OKGREEN}[2]{Colors.ENDC} Listar perguntas")
    print(f"{Colors.OKGREEN}[3]{Colors.ENDC} Responder pergunta")
    print(f"{Colors.OKGREEN}[4]{Colors.ENDC} Ver respostas de uma pergunta")
    print(f"{Colors.OKGREEN}[5]{Colors.ENDC} Trocar usuário")
    print(f"{Colors.OKGREEN}[0]{Colors.ENDC} Sair")
    print(border)
    return input(f"{Colors.BOLD}Escolha uma opção: {Colors.ENDC}")

def prompt_user_info():
    print(Colors.OKCYAN + '\n--- Informações do Usuário ---' + Colors.ENDC)
    name = input(f"{Colors.BOLD}Digite seu nome:{Colors.ENDC} ").strip()
    ra = input(f"{Colors.BOLD}Digite seu RA:{Colors.ENDC} ").strip()
    return name, ra

def display_questions(questions):
    print(Colors.OKCYAN + '\n--- Lista de Perguntas ---' + Colors.ENDC)
    if not questions:
        print(Colors.WARNING + 'Nenhuma pergunta registrada.' + Colors.ENDC)
    else:
        for q in questions:
            print(f"{Colors.BOLD}ID {q.id}:{Colors.ENDC} {q.text} {Colors.OKGREEN}(por {q.user} - RA {q.ra}){Colors.ENDC}")

def display_question_with_answers(q):
    print(Colors.OKCYAN + f"\n--- Pergunta ID {q.id} ---" + Colors.ENDC)
    print(f"{Colors.BOLD}{q.text}{Colors.ENDC} {Colors.OKGREEN}(por {q.user}){Colors.ENDC}")
    if not q.answers:
        print(Colors.WARNING + 'Nenhuma resposta ainda.' + Colors.ENDC)
    else:
        print(Colors.OKCYAN + '\nRespostas:' + Colors.ENDC)
        for i, a in enumerate(q.answers, 1):
            print(f"{Colors.OKGREEN}{i}.{Colors.ENDC} {a.text} {Colors.OKBLUE}(por {a.responder_name} - RA {a.responder_ra}){Colors.ENDC}")

def prompt_question_text():
    return input(f"{Colors.BOLD}Digite sua pergunta:{Colors.ENDC} ").strip()

def prompt_question_id():
    try:
        return int(input(f"{Colors.BOLD}Digite o ID da pergunta:{Colors.ENDC} ").strip())
    except ValueError:
        return None

def prompt_answer_text():
    return input(f"{Colors.BOLD}Digite sua resposta:{Colors.ENDC} ").strip()

def show_message(msg):
    print(f"{Colors.OKGREEN}{msg}{Colors.ENDC}")
