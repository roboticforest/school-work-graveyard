# File: TMQuestion.py

"""This module defines a class to represent a single question."""

class TMQuestion:

    MARKER = "-----"

    def __init__(self, name, text, answers):
        """Creates a new TMQuestion object with these attributes."""
        self._name = name
        self._text = text
        self._answers = answers

    def get_name(self):
        """Returns the name of this question."""
        return self._name

    def get_text(self):
        """Returns the list containing the text of this question."""
        return self._text

    def lookup_answer(self, response):
        """Looks up the response to find the next question."""
        next_question = self._answers.get(response, None)
        if next_question is None:
            next_question = self._answers.get("*", None)
        return next_question

    @staticmethod
    def read_question(f):
        """Reads one question from the data file f."""
        name = f.readline().rstrip()
        if name == "":
            return None
        text = [ ]
        finished = False
        while not finished:
            line = f.readline().rstrip()
            if line == TMQuestion.MARKER:
                finished = True
            else:
                text.append(line)
        answers = { }
        finished = False
        while not finished:
            line = f.readline().rstrip()
            if line == "":
                finished = True
            else:
                colon = line.find(":")
                if colon == -1:
                    raise ValueError("Missing colon in " + line)
                response = line[:colon].strip().upper()
                next_question = line[colon + 1:].strip()
                answers[response] = next_question
        return TMQuestion(name, text, answers)
