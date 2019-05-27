###notice hypothesis and premise
from allennlp.predictors.predictor import Predictor


from allennlp.predictors import Predictor
import json
from nltk import StanfordNERTagger,StanfordPOSTagger
#from nltk.parse.corenlp.CoreNLPParser import CoreNLPParser
from datetime import datetime
import nltk
import lucene
import re

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from pip._vendor.distlib.compat import raw_input
from java.io import File
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer

lucene.initVM()
stoplist =[',','.','\"','\n','The','the','-']
searcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File("./index/").toPath())))
def searchFunction(claim):##override
    analyzer = StandardAnalyzer()
    query = QueryParser("docName", analyzer).parse(claim)
    scoreDocs = searcher.search(query, 3).scoreDocs
    results = {}
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        if doc.get("docName") not in results.keys():
            results[doc.get("docName")]=(doc.get("docIndex"),doc.get("content"))
    #     else:
    #         if doc.get("docIndex") not in results.values()[0]:
    #             results[doc.get("docName")].append((doc.get("docIndex"),doc.get("content")))
    #
    # return results


predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/fine-grained-ner-model-elmo-2018.12.21.tar.gz")
valid_annotations = ['PERSON','FAC','ORG','PRODUCT','EVENT','WORK_OF_ART','LAW']
predictor_nlp = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/decomposable-attention-elmo-2018.02.19.tar.gz")

start = datetime.now()

with open("./Data/devset.json",'r') as trainset:
    with open('./new_allen.json', 'a',encoding='utf8') as newClaim:
        newClaim.write('{')
        total_dict = json.load(trainset)
        print(len(total_dict))
        l = 0
        for claimnum in total_dict.keys():
            total_claim = {}
            newClaim.write(
                "\"" + claimnum + "\"" + ':{' + '\n\t' + "\"claim\":" + "\"")
            for claim in list(total_dict[claimnum]["claim"]):
                if claim !='\"':
                    newClaim.write(claim+'')
                else:
                    newClaim.write('\\"')
            newClaim.write("\""
                + ',' + '\n\t' + "\"evidence\" : [")
            print('l', l)
            claimdoc = ''
            for word in total_dict[claimnum]["claim"]:
                word2=list(word)
                if '(' in word2:
                    claimdoc = claimdoc
                elif ')' in word2:
                    claimdoc =claimdoc
                if word=='(':
                    claimdoc+='-LRB-'
                elif word==')':
                    claimdoc+='-RRB-'
                elif word not in stoplist:
                    claimdoc += word
            print(claimdoc)
            allen_re=predictor.predict(sentence=claimdoc)
            word_list={}
            for word, tag in zip(allen_re['words'],allen_re['tags']):
                print(word,tag)
                if tag !='O':
                    tag=tag.split('-')[1]
                    if tag in valid_annotations:
                        if tag not in word_list.keys():
                            word_list[tag]=word
                        elif tag in word_list.keys():
                            word_list[tag]=word_list[tag]+'_'+word
            print(word_list)
            total_allen_re={}
            for allen_re in word_list.values():
                allen_result=searchFunction(allen_re)
                print('re',allen_result)
            #     for allen_result_re in allen_result:
            #         if allen_result_re not in total_allen_re:
            #             total_allen_re.append(allen_result_re)
            # print('t',total_allen_re)
            k = 0
            for re in total_allen_re:
                if k == len(total_allen_re) - 1:
                    newClaim.write('\n\t' + '[' + '\n\t' + "\"" + re + "\"" + '\n\t' + ']' + '\n')
                else:
                    newClaim.write('\n\t' + '[' + '\n\t' + "\"" + re + "\"" + '\n\t'+ '],' + '\n')
                    k += 1
            if l == len(total_dict) - 1:
                newClaim.write("]" + "\n" + "}" + "\n\t")
            else:
                newClaim.write("]" + "\n" + "}," + "\n\t")
            l+=1
        newClaim.write("}")
del searcher

newClaim.close()
trainset.close()
end = datetime.now()
print(end - start)