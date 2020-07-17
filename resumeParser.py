from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import operator
import threading

ignore_keywords = ['the', 'and', 'a', 'an', 'with', 'just', 'at', 'in', 'i', 'me', 'of', 'on', 'to', 'it', 'like', '.', ',', '\'', '\"', ';', '?', '!', '(', ')', '-', '*']

finance_keywords = ['finance', 'money', 'portfolio', 'stock', 'stocks', 'economics', 'firm', 'accounting', 'integrity', 'optimize', 'financed', 'analyze', 'growth',
                    'middle market', 'strategic', 'private equity', 'capital', 'evaluation']

humanResources_keywords = ['human resource', 'human resources', 'social work', 'communication', 'human', 'people', 'people skills', 'interpersonal', 'emotional',
            'diversity', 'budgeting', 'conflict resolution', 'conflict', 'decision making', 'consumer', 'managed', 'soft skills','manage',
            'teamwork','team building', 'team', 'cooperation', 'cooperate', 'logistics', 'organization', 'ethics', 'ethical', 'organize',
            'customer','relationship', 'management']

softwareDevelopment_keywords = ['cs', 'back end', 'backend', 'front end', 'frontend', 'full stack', 'full stack', 'application', 'features', 'data', 'analytics', 'analysis',
                                'data analytics', 'data analysis', 'data science', 'science', 'technology', 'security', 'cyber', 'computer', 'computer science', 'support',
                                'framework', 'terminal', 'java', 'python', 'github', 'developer', 'artificial intelligence', 'artificial', 'ai', 'it', 'machine learning',
                                'machine', 'virtual', 'cybersecurity', 'security', 'cyber', 'software', 'latex', 'mathematics', 'mips', 'assembly', 'c++', 'programming',
                                'program', 'code', 'coding', 'javascript', 'sql', 'robotic', 'robot', 'robotics', 'networking']

manufacturing_keywords = ['manufacturing', 'manufacture', 'mechanical engineering', 'mechanical', 'mechanics', 'engineering', 'civil engineering', 'civil engineer', 'civil',
                          'industrial', 'industrial engineering', 'robotic', 'robotics', 'construction', 'build', 'process', 'factory', 'industry', 'construct', 'oversee',
                          'supply chain', 'transport', 'vehicle', 'equipment', 'automate', 'machinery', 'machine', 'machines', 'robots', 'packaging']

frequencies = {'finance': 0, 'humanResources': 0, 'softwareDevelopment': 0, 'manufacturing': 0}

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

    text = text.lower()

    return text.split()

def parseFinance(text):
    val = 0
    for word in finance_keywords:
        if ' ' in word:
            arr = word.split()
            for i in range(len(text) - 1):
                if text[i] == arr[0] and text[i + 1] == arr[1]:
                    val += 1
        else:
            if word in text:
                val += text.count(word)

    frequencies['finance'] = val

def parseHumanResources(text):
    val = 0
    for word in humanResources_keywords:
        if ' ' in word:
            arr = word.split()
            for i in range(len(text) - 1):
                if text[i] == arr[0] and text[i + 1] == arr[1]:
                    val += 1
        else:
            if word in text:
                val += text.count(word)

    frequencies['humanResources'] = val

def parseSoftwareDevelopment(text):
    val = 0
    for word in softwareDevelopment_keywords:
        if ' ' in word:
            arr = word.split()
            for i in range(len(text) - 1):
                if text[i] == arr[0] and text[i + 1] == arr[1]:
                    val += 1
        else:
            if word in text:
                val += text.count(word)

    frequencies['softwareDevelopment'] = val

def parseManufacturing(text):
    val = 0
    for word in manufacturing_keywords:
        if ' ' in word:
            arr = word.split()
            for i in range(len(text) - 1):
                if text[i] == arr[0] and text[i + 1] == arr[1]:
                    val += 1
        else:
            if word in text:
                val += text.count(word)

    frequencies['manufacturing'] = val

def parseText(text):

    threads = []

    financeTask = threading.Thread(target=parseFinance, args=(text,))
    threads.append(financeTask)
    financeTask.start()

    humanResourcesTask = threading.Thread(target=parseHumanResources, args=(text,))
    threads.append(humanResourcesTask)
    humanResourcesTask.start()

    softwareDevelopmentTask = threading.Thread(target=parseSoftwareDevelopment, args=(text,))
    threads.append(softwareDevelopmentTask)
    softwareDevelopmentTask.start()

    manufacturingTask = threading.Thread(target=parseManufacturing, args=(text,))
    threads.append(manufacturingTask)
    manufacturingTask.start()

    for t in threads:
        t.join()

    result = max(frequencies.items(), key=operator.itemgetter(1))[0]

    strength = max(frequencies.items(), key=operator.itemgetter(1))[1] / len()
    if result == 'finance':
        strength /= len(finance_keywords)
    elif result == 'humanResources':
        strength /= len(humanResources_keywords)
    elif result == 'softwareDevelopment':
        strength /= len(softwareDevelopment_keywords)
    elif result == 'manufacturing':
        strength /= len(manufacturing_keywords)


    return result, strength

def categorize(resume):
    return parseText(extractPDFText(resume))