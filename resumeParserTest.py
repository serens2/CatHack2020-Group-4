import unittest
from resumeParser import extractPDFText
from resumeParser import categorize

class resumeParserTest(unittest.TestCase):
    def testTextExtraction(self):
        hiText = extractPDFText('examplePDFs/Hi.pdf')
        self.assertEqual(hiText, ['Hi','Hello', 'how', 'are', 'you', 'I’m', 'good', 'thanks', 'Sick'])

    def testSDExampel(self):
        result = categorize('examplePDFs/SDExample.pdf')
        self.assertEqual("softwareDevelopment", result)

if __name__ == '__main__':
    unittest.main()