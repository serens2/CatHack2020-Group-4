import unittest
from resumeParser import extractPDFText

class resumeParserTest(unittest.TestCase):
    def testBasic(self):
        hiText = extractPDFText('examplePDFs/Hi.pdf')
        self.assertEqual(hiText, ['Hi','Hello', 'how', 'are', 'you', 'I’m', 'good', 'thanks', 'Sick'])

if __name__ == '__main__':
    unittest.main()