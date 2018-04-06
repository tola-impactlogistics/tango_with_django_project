import PyPDF2 
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def searchInPDF(filename, key):
    occurrences = 0
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    if text != "":
        text = text
    else:
        text = textract.process(filename, method='tesseract', language='eng')
    #tokens = word_tokenize(text)
    tokens = [m for m in text.split()]
    punctuation = ['(',')',';',':','[',']',',']
    #stop_words = stopwords.words('english')
    keywords = [word for word in tokens if not word in punctuation]
    for k in keywords:
        if key == k: occurrences+=1
    return occurrences 

def path_to(filename):
    global completePath
    global stackf
    import os, sys
    path = r'C:\Users\User\Desktop\Contact'
    #finally:
    #    path = (r'C:\Users\User\Desktop\%s' %(filee))
    completePath = os.path.join(path, filename) # completePath is a string
    return completePath
path_to("Oracle Essentials Oracle Database 10g.pdf")
count = searchInPDF(completePath, "Relational")
print(count)