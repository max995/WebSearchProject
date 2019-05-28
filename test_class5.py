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
stoplist =[',','.','\"','\n','The','the','\'',':']
searcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File("./index/").toPath())))

def searchFunction(claim):
    analyzer = StandardAnalyzer()
    query = QueryParser("docName", analyzer).parse(claim)
    scoreDocs = searcher.search(query, 5).scoreDocs
    #print("%s total matching documents." % len(scoreDocs))
    results = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        if doc.get("docName") not in results:
            results.append(doc.get("docName"))
    return results


predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/fine-grained-ner-model-elmo-2018.12.21.tar.gz")
valid_annotations_pre = ['PERSON','FAC','ORG','PRODUCT','EVENT','WORK_OF_ART','LAW']
valid_annotations=['NORP','GPE','LOC','LANGUAGE']
valid_annotations_pre1 = '[B|I|U|L]-|PERSON|FAC|ORG|PRODUCT|EVENT|WORK_OF_ART|LAW'
re.compile(valid_annotations_pre1)
valid_annotations1='[B|I|U|L]-|NORP|GPE|LOC|LANGUAGE'
re.compile(valid_annotations1)
jar='/Users/agatha/anaconda3/lib/python3.7/site-packages/stanford-ner-2018-10-16/stanford-ner.jar'
st1= StanfordPOSTagger(model_filename='/Users/agatha/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger', path_to_jar='/Users/agatha/stanford-postagger-full-2015-04-20/stanford-postagger.jar')
start = datetime.now()

def get_allen_result(allen_re_v):
    v_pre=0
    v_flag=0
    tags_v=allen_re_v['tags']
    print(tags_v)
    words3=allen_re_v['words']
    #print(words3)
    tags = []
    for tags1 in tags_v:
        tags1_list = list(tags1)
        if '-' in tags1_list:
            #print(tags1)
            tags.append((tags1.split('-')[0], tags1.split('-')[1]))
        else:
            tags.append(('O', tags1))
    for tt in tags:
        if tt[1] in valid_annotations_pre:
            v_pre+=1
        elif tt[1] in valid_annotations:
            v_flag+=1
    print('v_pre',v_pre,'v_flag',v_flag)
    wordlist = {}
    if v_pre !=0:
        phrase = ''
        for word, tag in zip(allen_re_v['words'], allen_re_v['tags']):
            tag_list = list(tag)
            if '-' in tag_list:
                tag = tag.split('-')
                if bool(re.match(valid_annotations_pre1,tag[1])):
                    if tag[1] not in wordlist.keys():
                        wordlist[tag[1]] = []
                        if 'U' in tag[0]:
                            wordlist[tag[1]].append(word)
                        elif 'B' in tag[0]:
                            phrase = word
                        elif 'I' in tag[0]:
                            phrase += '_' + word
                        elif 'L' in tag[0]:
                            phrase += '_' + word
                            wordlist[tag[1]].append(phrase)
                            phrase = ''
                    else:
                        if 'U' in tag[0]:
                            wordlist[tag[1]].append(word)
                        elif 'B' in tag[0]:
                            phrase = word
                        elif 'I' in tag[0]:
                            phrase += '_' + word
                        elif 'L' in tag[0]:
                            phrase += '_' + word
                            wordlist[tag[1]].append(phrase)
                            phrase = ''
    elif v_flag !=0 and v_pre==0:
        phrase = ''
        for word, tag in zip(allen_re_v['words'], allen_re_v['tags']):
            tag_list = list(tag)
            if '-' in tag_list:
                tag = tag.split('-')
                if bool(re.match(valid_annotations1, tag[1])):
                    if tag[1] not in wordlist.keys():
                        wordlist[tag[1]] = []
                        if 'U' in tag[0]:
                            wordlist[tag[1]].append(word)
                        elif 'B' in tag[0]:
                            phrase = word
                        elif 'I' in tag[0]:
                            phrase += '_' + word
                        elif 'L' in tag[0]:
                            phrase += '_' + word
                            wordlist[tag[1]].append(phrase)
                            phrase = ''
                    else:
                        if 'U' in tag[0]:
                            wordlist[tag[1]].append(word)
                        elif 'B' in tag[0]:
                            phrase = word
                        elif 'I' in tag[0]:
                            phrase += '_' + word
                        elif 'L' in tag[0]:
                            phrase += '_' + word
                            wordlist[tag[1]].append(phrase)
                            phrase = ''
    elif v_flag==0 and v_pre==0:
        words_str=''
        st_re =[]
        for raw_word in words3:
            words_str +=raw_word+' '
        st_re = st1.tag(words_str.split())
        st_tag = []
        st_word = []
        for st_pair in st_re:
            st_tag.append(st_pair[1])
            st_word.append(st_pair[0])
        wordlist = {'NNP': []}
        j = 0
        while j < (len(st_tag)):
            if st_tag[j] == 'NNP':
                shortTerm = st_word[j]
                k = j + 1
                for j1 in range(k, len(st_tag)):
                    if st_tag[j1] == 'NNP':
                        shortTerm += '_' + st_word[j1]
                        j = j + 1
                    else:
                        break
                wordlist['NNP'].append(shortTerm)
            j = j + 1
    return wordlist

def main():
    try:
        with open("./Data/test-unlabelled.json",'r',encoding='utf8') as trainset:
            with open('./allen_test_5.json', 'a',encoding='utf8') as newClaim:
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
                            claimdoc=claimdoc
                        elif word==')':
                            claimdoc=claimdoc
                        elif word not in stoplist:
                            claimdoc += word
                    print(claimdoc)
                    allen_re=predictor.predict(sentence=claimdoc)
                    word_list={}
                    word_list=get_allen_result(allen_re)
                    print(word_list)
                    total_allen_re=[]
                    try:
                        for allen_re_re in word_list.values():
                            for allen_re in allen_re_re:
                                allen_result=searchFunction(allen_re)
                                print('re',allen_result)
                                for allen_result_re in allen_result:
                                    if allen_result_re not in total_allen_re:
                                        total_allen_re.append(allen_result_re)
                        print('t',total_allen_re)
                    except Exception as e:
                        print(e)
                    k = 0
                    for re1 in total_allen_re:
                        re_str=list(re1)
                        newClaim.write('\n\t' + '[' + '\n\t' + "\"" )
                        if '\"' in re_str:
                            for re_re_str in re_str:
                                if re_re_str =='\"':
                                    newClaim.write('\\"')
                                else:
                                    newClaim.write(re_re_str)
                            if k == len(total_allen_re) - 1:
                                newClaim.write("\"" + '\n\t' + ']' + '\n')
                            else:
                                newClaim.write( "\"" + '\n\t'+ '],' + '\n')
                                k += 1
                        else:
                            if k == len(total_allen_re) - 1:
                                newClaim.write(re1 + "\"" + '\n\t' + ']' + '\n')
                            else:
                                newClaim.write(re1 + "\"" + '\n\t'+ '],' + '\n')
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
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()