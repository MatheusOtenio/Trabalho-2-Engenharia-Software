# model.py

class Question:
    def __init__(self, id, ra, user, text):
        self.id = id
        self.ra = ra
        self.user = user
        self.text = text
        self.answers = []

class Answer:
    def __init__(self, question_id, responder_ra, responder_name, text):
        self.question_id = question_id
        self.responder_ra = responder_ra
        self.responder_name = responder_name
        self.text = text