# controller.py
from repository import CsvRepositoryAdapter
from model import Question, Answer
from view import clear_screen, show_menu, pause, prompt_user_info, show_message, display_questions, display_question_with_answers, prompt_question_id, prompt_question_text, prompt_answer_text


def run():
    repo = CsvRepositoryAdapter()
    questions = repo.load_questions()
    repo.load_answers(questions)

    clear_screen()
    user, ra = prompt_user_info()

    running = True

    while running:
        clear_screen()
        choice = show_menu()

        if choice == '1':
            clear_screen()
            text = prompt_question_text()
            q = Question(repo.get_next_id(questions), ra, user, text)
            repo.save_question(q)
            questions.append(q)
            show_message(f"Pergunta registrada com ID {q.id}.")
            pause()

        elif choice == '2':
            clear_screen()
            display_questions(questions)
            pause()

        elif choice == '3':
            clear_screen()
            display_questions(questions)
            qid = prompt_question_id()
            if qid is None:
                show_message('ID inválido.')
                pause()
                continue
            q = next((q for q in questions if q.id == qid), None)
            if not q:
                show_message('Pergunta não encontrada.')
                pause()
                continue
            clear_screen()
            display_question_with_answers(q)
            text = prompt_answer_text()
            a = Answer(qid, ra, user, text)
            repo.save_answer(a)
            q.answers.append(a)
            show_message('Resposta registrada com sucesso!')
            pause()

        elif choice == '4':
            clear_screen()
            display_questions(questions)
            qid = prompt_question_id()
            if qid is None:
                show_message('ID inválido.')
                pause()
                continue
            q = next((q for q in questions if q.id == qid), None)
            if not q:
                show_message('Pergunta não encontrada.')
                pause()
                continue
            clear_screen()
            display_question_with_answers(q)
            pause()

        elif choice == '5':
            clear_screen()
            user, ra = prompt_user_info()
            show_message(f"Usuário atualizado para {user} (RA {ra}).")
            pause()

        elif choice == '0':
            running = False

        else:
            show_message('Opção inválida. Tente novamente.')
            pause()
