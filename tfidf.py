import codecs
import jieba
import math
import argparse

class Document:
    def __init__(self, document, needSegment, stopwords):
        words = []
        if needSegment:
            segment = jieba.cut(document)
            for word in segment:
                word = word.lower().strip()
                if word not in stopwords and len(word) > 1:
                    words.append(word)
        else:
            words = document.split(" ")
        self.M = len(words)
        self.term2count = {}
        for word in words:
            if word in self.term2count.keys():
                self.term2count[word] += 1
            else:
                self.term2count[word] = 1
            

class Tfidf:
    def __init__(self, documentsFilePath, outputDirectory = "", stopwordsFilePath = None, K = 10, needSegment = True, multiline = True):
        self.documentsFilePath = documentsFilePath
        self.outputDirectory = outputDirectory
        self.stopwordsFilePath = stopwordsFilePath
        self.K = K
        self.needSegment = needSegment
        self.multiline = multiline
        self.stopwords = set()
        if self.stopwordsFilePath != None:
            for word in codecs.open(self.stopwordsFilePath, 'r', 'utf-8'):
                self.stopwords.add(word.lower().strip())
        self.docs = []
        for document in codecs.open(self.documentsFilePath, 'r', 'utf-8'):
            self.docs.append(Document(document, self.needSegment, self.stopwords))
        self.N = len(self.docs)
        
    def execute(self):
        dictionary = set()
        for doc in self.docs:
            for word in doc.term2count.keys():
                dictionary.add(word)
        self.term2df = {}
        for word in dictionary:
            for doc in self.docs:
                if word in doc.term2count.keys():
                    if(word in self.term2df.keys()):
                        self.term2df[word] += 1
                    else:
                        self.term2df[word] = 1

        file = codecs.open(self.outputDirectory + "/keywords.txt", 'w', 'utf-8')
        for doc in self.docs:
            term2tfidf = {}
            for word in doc.term2count.keys():
                tf = 1.0 * doc.term2count[word] / doc.M
                idf = math.log(1.0 * self.N / self.term2df[word])
                tfidf = tf * idf
                term2tfidf[word] = tfidf
            items = [[item[1], item[0]] for item in term2tfidf.items()]
            items.sort(reverse = True)
            keywords = [items[i][1] for i in range(0, min(len(items), self.K))]
            if self.multiline:
                for i in range(0, len(keywords)):
                    if i == 0:
                        file.write(keywords[i])
                    else:
                        file.write(" " + keywords[i])
                    if i == len(keywords)-1:
                        file.write("\n")
            else:
                for i in range(0, len(keywords)):
                    file.write(keywords[i] + "\n")
        file.close()
        
def readParamsFromCmd():
    parser = argparse.ArgumentParser(description = "This is a python implementation of tfidf to extract keywords of documents. Support both English and Chinese. A line in the input represents a document.")
    parser.add_argument('documentsFilePath', help = 'The file path of input documents.')
    parser.add_argument('-o', '--outputDirectory', help = 'The directory of output keywords. (default current dir)')
    parser.add_argument('-s', '--stopwordsFilePath', help = 'The file path of stopwords, each line represents a word.', default = None)
    parser.add_argument('-k', type = int, help = 'The number of keywords of each document to generate (default 10).', default = 10)
    parser.add_argument('--seg', type = bool, help = 'Whether the documents has to be segmented (default true).', default = True)
    parser.add_argument('-m', type = bool, help = 'Whether output the keywords in multi lines. If true, a line contains the keywords of only one document, otherwise all. (default true)', default = True)
    return parser.parse_args()
        
params = readParamsFromCmd().__dict__
tfidf = Tfidf(params['documentsFilePath'], outputDirectory = params['outputDirectory'], stopwordsFilePath = params['stopwordsFilePath'], K = params['k'], needSegment = params['seg'], multiline = params['m'])
tfidf.execute()
print('finished')