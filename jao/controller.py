# controller.py
# Controller: Gerencia o fluxo da aplicação e coordena Model e View

from repository import CsvRepositoryAdapter
from model import Question, Answer
from view import clear_screen, show_menu, pause, prompt_user_info, show_message, display_questions, display_question_with_answers, prompt_question_id, prompt_question_text, prompt_answer_text


def run():
    """
    Função principal do controller que gerencia todo o fluxo da aplicação.
    Responsável por:
    1. Inicializar o repositório usando o padrão Adapter
    2. Carregar os dados existentes
    3. Gerenciar o loop principal do programa
    4. Coordenar as interações entre Model e View
    """
    # Inicialização do repositório e carregamento dos dados
    repo = CsvRepositoryAdapter()
    questions = repo.load_questions()
    repo.load_answers(questions)

    # Configuração inicial do usuário
    clear_screen()
    user, ra = prompt_user_info()

    running = True

    # Loop principal do programa
    while running:
        clear_screen()
        choice = show_menu()

        if choice == '1':  # Nova pergunta
            clear_screen()
            text = prompt_question_text()
            # Cria nova instância de Question (Model)
            q = Question(repo.get_next_id(questions), ra, user, text)
            # Persiste no repositório e atualiza lista em memória
            repo.save_question(q)
            questions.append(q)
            show_message(f"Pergunta registrada com ID {q.id}.")
            pause()

        elif choice == '2':  # Listar perguntas
            clear_screen()
            display_questions(questions)
            pause()

        elif choice == '3':  # Responder pergunta
            clear_screen()
            display_questions(questions)
            # Validação do ID da pergunta
            qid = prompt_question_id()
            if qid is None:
                show_message('ID inválido.')
                pause()
                continue
            # Busca a pergunta na lista
            q = next((q for q in questions if q.id == qid), None)
            if not q:
                show_message('Pergunta não encontrada.')
                pause()
                continue
            # Processo de resposta
            clear_screen()
            display_question_with_answers(q)
            text = prompt_answer_text()
            # Cria nova instância de Answer (Model)
            a = Answer(qid, ra, user, text)
            # Persiste no repositório e atualiza em memória
            repo.save_answer(a)
            q.answers.append(a)
            show_message('Resposta registrada com sucesso!')
            pause()

        elif choice == '4':  # Ver respostas
            clear_screen()
            display_questions(questions)
            # Validação do ID da pergunta
            qid = prompt_question_id()
            if qid is None:
                show_message('ID inválido.')
                pause()
                continue
            # Busca e exibe a pergunta com suas respostas
            q = next((q for q in questions if q.id == qid), None)
            if not q:
                show_message('Pergunta não encontrada.')
                pause()
                continue
            clear_screen()
            display_question_with_answers(q)
            pause()

        elif choice == '5':  # Trocar usuário
            clear_screen()
            user, ra = prompt_user_info()
            show_message(f"Usuário atualizado para {user} (RA {ra}).")
            pause()

        elif choice == '0':  # Sair
            running = False

        else:  # Opção inválida
            show_message('Opção inválida. Tente novamente.')
            pause()
