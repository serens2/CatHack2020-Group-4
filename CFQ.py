from resumeParser import extractPDFText
from resumeParser import categorize

import requests
import queue

def main():
    test2()


def test1():
    claire = Applicant('Claire', 'cmboyan@gmail.com', 'Senior', 'CS', True, 'examplePDFs/resume.pdf')
    tyler = Applicant('Tyler', 'tyatcat@gmail.com', 'Senior', 'Mechanical Engineering', False, 'examplePDFs/tyler.pdf')
    sam = Applicant('Sam', 'serens@gmail.com', 'Junior', 'Math', False, 'examplePDFs/sam.pdf')
    andrew = Applicant('Andrew', 'alu@gmail.com', 'Senior', 'Business', True, 'examplePDFs/andrew.pdf')

    q = Line()
    q.add(claire)
    q.add(tyler)
    q.add(sam)
    q.add(andrew)

    q.display()

def test2():
    claire = Applicant('Claire', 'cmboyan@gmail.com', 'Senior', 'CS', True, 'examplePDFs/resume.pdf')
    tyler = Applicant('Tyler', 'tyatcat@gmail.com', 'Senior', 'Mechanical Engineering', False, 'examplePDFs/tyler.pdf')
    sam = Applicant('Sam', 'serens@gmail.com', 'Junior', 'Math', False, 'examplePDFs/sam.pdf')
    andrew = Applicant('Andrew', 'alu@gmail.com', 'Senior', 'Business', True, 'examplePDFs/andrew.pdf')

    q = Line()
    q.add(claire)
    q.add(tyler)
    q.add(sam)
    q.add(andrew)

    q.display()
    print('\n\n\n')
    q.pop()
    print('\n\n\n')
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
        self.color = self.pick_color(self.vertical)

    def assign_vertical(self):
        self.vertical, score = categorize(self.resume)
        return self.vertical, score

    def score_strength(self, score):
        if score > 0.45:
            return 'strongly'
        else:
            return 'weakly'

    def pick_color(self, vert):
        color = 'Red'
        if vert == 'finance':
            color = 'Red'
        elif vert == 'humanResources':
            color = 'Orange'
        elif vert == 'softwareDevelopment':
            color = 'Blue'
        elif vert == 'manufactoring':
            color = 'Green'
        return color

    def display(self):
        info = '''Applicant {} is a {} in {}.
You can contact them at {}.
Applicant {} matches with {}.
Applicant is looking for the color {}'''.format(self.name, self.year, self.major, self.email, self.strength, self.vertical, self.color)
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
            print('Now helping:')
            next_in_line.display()

    def add(self, app):
        current_line = self.q
        if app in current_line:
            print('You are already in line')
        else:
            self.q.append(app)

    def display(self):
        print('Current Queue')
        print('--------------------------------')
        disp = [x for x in self.q]
        disp.reverse()
        for wait in disp:
            wait.display()
            print('--------------------------------')



if __name__ == "__main__":
    main()