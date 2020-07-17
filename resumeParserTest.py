import unittest
from resumeParser import extractPDFText
from resumeParser import categorize

class resumeParserTest(unittest.TestCase):
    def testTextExtraction(self):
        hiText = extractPDFText('examplePDFs/Hi.pdf')
        self.assertEqual(hiText, ['hi','hello', 'how', 'are', 'you', 'i’m', 'good', 'thanks', 'sick'])

    def testSDExampel(self):
        result = categorize('examplePDFs/SDExample.pdf')
        self.assertEqual('softwareDevelopment', result)

    def testClaireResume(self):
        result = categorize('examplePDFs/resume.pdf')
        self.assertEqual('softwareDevelopment', result)

if __name__ == '__main__':
    unittest.main()