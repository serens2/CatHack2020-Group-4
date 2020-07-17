from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import operator

ignore_keywords = ['the', 'and', 'a', 'an', 'with', 'just', 'at', 'in', 'I', 'me', 'of', 'on', 'to', 'it', 'like', '.', ',', '\'', '\"', ';', '?', '!', '(', ')', '-', '*']
finance_keywords = ['finance', 'money', 'portfolio', 'stock', 'stocks', 'economics', 'firm', 'accounting']
humanResources_keywords = ['human resource', 'human resources', 'social work', 'communication', 'human', 'people', 'people skills', 'interpersonal', 'emotional', 'diversity']
softwareDevelopment_keywords = ['cs', 'back end', 'backend', 'front end', 'frontend', 'full stack', 'full stack', 'application', 'features', 'data', 'analytics', 'analysis',
                       'data analytics', 'data analysis', 'data science', 'science', 'technology', 'security', 'cyber', 'computer', 'computer science', 'support',
                       'framework', 'terminal', 'java', 'python', 'github', 'developer', 'artificial intelligence', 'artificial', 'ai', 'it', 'machine learning', 'machine',
                       'virtual', 'cybersecurity', 'security', 'cyber']
manufacturing_keywords = []

def extractPDFText(filename):

    # following code snippet adapted from
    # https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(filename, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ''
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text.split()

def parseText(text):
    frequencies = {'finance' : 0, 'humanResources' : 0, 'softwareDevelopment' : 0, 'manufacturing' : 0}

    for word in text:
        if word.lower() in ignore_keywords:
            continue
        if word.lower() in finance_keywords:
            frequencies['finance'] = frequencies.get('finance') + 1
        if word.lower() in humanResources_keywords:
            frequencies['humanResources'] = frequencies.get('humanResources') + 1
        if word.lower() in softwareDevelopment_keywords:
            frequencies['softwareDevelopment'] = frequencies.get('softwareDevelopment') + 1
        if word.lower() in manufacturing_keywords:
            frequencies['manufacturing'] = frequencies.get('manufacturing') + 1
    result = max(frequencies.items(), key=operator.itemgetter(1))[0]
    return result

def categorize(resume):
    return parseText(extractPDFText(resume))