# Repository: Implementação do padrão Adapter para persistência em CSV

import csv
import os
from model import Question, Answer

# Configuração dos arquivos CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, 'questions.csv')
ANSWERS_FILE = os.path.join(BASE_DIR, 'answers.csv')

class QuestionRepositoryInterface:
    # Interface base para repositório de perguntas
    def load_questions(self): raise NotImplementedError
    def load_answers(self, questions): raise NotImplementedError
    def save_question(self, question): raise NotImplementedError
    def save_answer(self, answer): raise NotImplementedError
    def get_next_id(self, questions): raise NotImplementedError

class CsvRepositoryAdapter(QuestionRepositoryInterface):
    # Adapter para persistência em arquivos CSV
    def __init__(self):
        # Cria arquivos CSV se não existirem
        if not os.path.exists(QUESTIONS_FILE):
            with open(QUESTIONS_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id','RA','user','text'])
                writer.writeheader()
        if not os.path.exists(ANSWERS_FILE):
            with open(ANSWERS_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['question_id','responder_RA','responder_name','text'])
                writer.writeheader()

    def load_questions(self):
        # Carrega perguntas do CSV
        questions = []
        with open(QUESTIONS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                questions.append(Question(int(row['id']), row['RA'], row['user'], row['text']))
        return questions

    def load_answers(self, questions):
        # Carrega e associa respostas às perguntas
        with open(ANSWERS_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                a = Answer(int(row['question_id']), row['responder_RA'], row['responder_name'], row['text'])
                for q in questions:
                    if q.id == a.question_id:
                        q.answers.append(a)
                        break

    def save_question(self, question):
        # Persiste nova pergunta no CSV
        with open(QUESTIONS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id','RA','user','text'])
            writer.writerow({'id': question.id, 'RA': question.ra, 'user': question.user, 'text': question.text})

    def save_answer(self, answer):
        # Persiste nova resposta no CSV
        with open(ANSWERS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['question_id','responder_RA','responder_name','text'])
            writer.writerow({'question_id': answer.question_id,
                             'responder_RA': answer.responder_ra,
                             'responder_name': answer.responder_name,
                             'text': answer.text})

    def get_next_id(self, questions):
        # Gera próximo ID disponível
        existing = [q.id for q in questions]
        return max(existing, default=0) + 1