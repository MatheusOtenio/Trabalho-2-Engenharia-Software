#!/usr/bin/env python3

"""
Sistema de fórum de perguntas e respostas em terminal.
Interface amigável sem dependências externas.
"""
import csv
import os
import platform

def clear_screen():
    # Limpa a tela de forma cross-platform
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Diretório base: onde o script está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, 'questions.csv')
ANSWERS_FILE = os.path.join(BASE_DIR, 'answers.csv')


def load_data():
    questions = []
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            has_id = 'id' in (reader.fieldnames or [])
            for idx, row in enumerate(reader, start=1):
                qid = int(row['id']) if has_id and row.get('id') else idx
                questions.append({
                    'id': qid,
                    'RA': row.get('RA', ''),
                    'user': row.get('user', ''),
                    'text': row.get('text', ''),
                    'answers': []
                })
    if os.path.exists(ANSWERS_FILE):
        with open(ANSWERS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    qid = int(row.get('question_id', 0))
                except ValueError:
                    continue
                for q in questions:
                    if q['id'] == qid:
                        q['answers'].append({
                            'responder_RA': row.get('responder_RA', ''),
                            'responder_name': row.get('responder_name', ''),
                            'text': row.get('text', '')
                        })
                        break
    return questions


def ensure_csv_files():
    if not os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id','RA','user','text'])
            writer.writeheader()
    if not os.path.exists(ANSWERS_FILE):
        with open(ANSWERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['question_id','responder_RA','responder_name','text'])
            writer.writeheader()


def get_next_id(questions):
    existing = [q['id'] for q in questions]
    return max(existing, default=0) + 1


def pause():
    input("\nPressione Enter para continuar...")


def main():
    ensure_csv_files()
    questions = load_data()
    next_id = get_next_id(questions)

    clear_screen()
    print("=== Fórum de Perguntas e Respostas ===")
    current_user = input("Digite seu nome: ").strip()
    current_RA = input("Digite seu RA: ").strip()

    while True:
        clear_screen()
        print("--- Menu Principal ---")
        print("1. Fazer pergunta")
        print("2. Listar perguntas")
        print("3. Responder pergunta")
        print("4. Ver respostas de uma pergunta")
        print("5. Trocar usuário")
        print("0. Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == '1':
            clear_screen()
            print("--- Nova Pergunta ---")
            text = input("Digite sua pergunta: ").strip()
            with open(QUESTIONS_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id','RA','user','text'])
                writer.writerow({'id': next_id, 'RA': current_RA, 'user': current_user, 'text': text})
            questions.append({'id': next_id, 'RA': current_RA, 'user': current_user, 'text': text, 'answers': []})
            print(f"Pergunta registrada com ID {next_id}.")
            next_id += 1
            pause()

        elif choice == '2':
            clear_screen()
            print("--- Lista de Perguntas ---")
            if not questions:
                print("Nenhuma pergunta registrada.")
            else:
                for q in questions:
                    print(f"ID {q['id']}: {q['text']} (por {q['user']} - RA {q['RA']})")
            pause()

        elif choice == '3':
            clear_screen()
            print("--- Responder Pergunta ---")
            if not questions:
                print("Nenhuma pergunta disponível.")
                pause()
                continue
            try:
                qid = int(input("Digite o ID da pergunta: ").strip())
            except ValueError:
                print("ID inválido.")
                pause()
                continue
            selected = next((q for q in questions if q['id'] == qid), None)
            if not selected:
                print("Pergunta não encontrada.")
                pause()
                continue
            print(f"Pergunta: {selected['text']} (por {selected['user']})")
            answer_text = input("Digite sua resposta: ").strip()
            with open(ANSWERS_FILE,'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['question_id','responder_RA','responder_name','text'])
                writer.writerow({'question_id': qid, 'responder_RA': current_RA, 'responder_name': current_user, 'text': answer_text})
            selected['answers'].append({'responder_RA': current_RA, 'responder_name': current_user, 'text': answer_text})
            print("Resposta registrada com sucesso!")
            pause()

        elif choice == '4':
            clear_screen()
            print("--- Visualizar Respostas ---")
            if not questions:
                print("Nenhuma pergunta registrada.")
                pause()
                continue
            try:
                qid = int(input("Digite o ID da pergunta: ").strip())
            except ValueError:
                print("ID inválido.")
                pause()
                continue
            selected = next((q for q in questions if q['id'] == qid), None)
            if not selected:
                print("Pergunta não encontrada.")
                pause()
                continue
            print(f"Pergunta: {selected['text']} (por {selected['user']})")
            if not selected['answers']:
                print("Nenhuma resposta ainda.")
            else:
                for i,a in enumerate(selected['answers'],1):
                    print(f"{i}. {a['text']} (por {a['responder_name']} - RA {a['responder_RA']})")
            pause()

        elif choice == '5':
            clear_screen()
            print("--- Trocar Usuário ---")
            current_user = input("Digite seu nome: ").strip()
            current_RA = input("Digite seu RA: ").strip()
            print(f"Usuário atualizado para {current_user} (RA {current_RA}).")
            time.sleep(1)

        elif choice == '0':
            clear_screen()
            print("Obrigado por usar o fórum! Até mais.")
            break

        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)

if __name__ == "__main__":
    main()
