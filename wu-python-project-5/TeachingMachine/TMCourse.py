# File: TMCourse.py

"""This module defines a class to represent a TeachingMachine course."""

from TMQuestion import TMQuestion

class TMCourse:

    def __init__(self, questions):
        """Creates a new TMCourse object with the specified questions."""
        self._questions = questions

    def get_question(self, name):
        """Returns the question with the specified name."""
        return self._questions[name]

    def run(self):
        """Steps through the questions in this course."""
        current = "START"
        while current != "EXIT":
            question = self.get_question(current)
            for line in question.get_text():
                print(line)
            answer = input("> ").strip().upper()
            next = question.lookup_answer(answer)
            if next is None:
                print("I don't understand that response.")
            else:
                current = next

# Implementation notes
# --------------------
# To make sure that the course starts at the first question, this method
# always includes an entry labeled "START" in the question table.

    @staticmethod
    def read_course(f):
        """Reads the entire course from the data file f."""
        questions = { }
        finished = False
        while not finished:
            question = TMQuestion.read_question(f)
            if question is None:
                finished = True
            else:
                name = question.get_name()
                if len(questions) == 0:
                    questions["START"] = question
                questions[name] = question
        return TMCourse(questions)
