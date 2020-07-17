from resumeParser import extractPDFText
from resumeParser import categorize

import requests
import queue

def main():
    claire = Applicant('Claire', 'cmboyan@gmail.com', 'Senior', 'CS', True, 'examplePDFs/claire.pdf')
    tyler = Applicant('Tyler', 'tyatcat@gmail.com', 'Senior', 'Mechanical Engineering', False, 'examplePDFs/tyler.pdf')
    sam = Applicant('Sam', 'serens@gmail.com', 'Junior', 'Math', False, 'examplePDFs/sam.pdf')
    noah = Applicant('Noah', 'noahi2@gmail.com', 'Senior', 'CS', True, 'examplePDFs/noah.pdf')

    q = Line()
    q.add(claire)
    q.add(tyler)
    q.add(sam)
    q.add(noah)

    q.display()


class Applicant:
    def __init__(self, name, email, year, major, reference, resume):
        # Given
        self.name = name
        self.email = email
        self.year = year
        self.major = major
        self.reference = reference
        self.resume = resume

        # Calculated
        self.vertical, score = self.assign_vertical()
        self.strength = self.score_strength(score)
        self.color = self.pick_color()

    def assign_vertical(self):
        self.vertical, score = categorize(self.resume)
        return self.vertical, score

    def score_strength(self, score):
        print(score)
        if score > 0.8:
            return 'strongly'
        else:
            return 'weakly'

    def pick_color(self):
        return 'Red'

    def display(self):
        info = '''Applicant {} is a {} in {}.
You can contact them at {}.
Applicant {} matches with {}.'''.format(self.name, self.year, self.major, self.email, self.strength, self.vertical)
        if self.reference:
            print(info + '\nApplicant does have a reference.')
        else:
            print(info)



class Line:
    def __init__(self):
        self.q = []

    def pop(self):
        current_line = self.q
        if len(current_line) == 0:
            print('There is no one in line')
        else:
            next_in_line = current_line.pop()
            next_in_line.display()

    def add(self, app):
        current_line = self.q
        if app in current_line:
            print('You are already in line')
        else:
            self.q.append(app)

    def display(self):
        print('--------------------------------')
        for wait in self.q:
            wait.display()
            print('--------------------------------')



if __name__ == "__main__":
    main()