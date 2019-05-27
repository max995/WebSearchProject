import json
from nltk import StanfordNERTagger,StanfordPOSTagger
#from nltk.parse.corenlp.CoreNLPParser import CoreNLPParser
from datetime import datetime
import nltk
import lucene

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from pip._vendor.distlib.compat import raw_input
from java.io import File
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer

lucene.initVM()
stoplist =[',','.','\"','\n',':','/','-']
#changelist=[('(','-LRB-'),(')','-RRB')]
searcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File("./index/").toPath())))
def searchFunction(claim):
    analyzer = StandardAnalyzer()
    query = QueryParser("docName", analyzer).parse(claim)
    scoreDocs = searcher.search(query, 5).scoreDocs
    #print("%s total matching documents." % len(scoreDocs))
    results = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        # print("name", doc.get("name"),
        #       "docName", doc.get("docName"))
        wp=[]
        if doc.get("docName") not in results:
            wp=list(doc.get("docName"))
            if '\"'  not in wp:
                results.append(doc.get("docName"))
            else:
                results.append(['\"'+doc.get("docName")+'\"'])

    return results




jar='/Users/agatha/anaconda3/lib/python3.7/site-packages/stanford-ner-2018-10-16/stanford-ner.jar'
st1= StanfordPOSTagger(model_filename='/Users/agatha/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger', path_to_jar='/Users/agatha/stanford-postagger-full-2015-04-20/stanford-postagger.jar')
start = datetime.now()

with open("./Data/devset.json",'r') as trainset:
    with open('./new_claim_stanford.json', 'a') as newClaim:
        newClaim.write('{')
        total_dict=json.load(trainset)
        print(len(total_dict))
        l=0
        for claimnum in total_dict.keys():
            total_claim={}
            newClaim.write(
                "\"" + claimnum + "\"" + ':{' + '\n\t' + "\"claim\":" + "\"")
            for claim in list(total_dict[claimnum]["claim"]):
                if claim != '\"':
                    newClaim.write(claim + '')
                else:
                    newClaim.write('\\"')
            newClaim.write("\""
                           + ',' + '\n\t' + "\"evidence\" : [")
            #total_claim[claimnum] ={"claim":total_dict[claimnum]["claim"],"evidence":[]}
            print('l',l)
            claimdoc=''
            for word in total_dict[claimnum]["claim"]:
                word1=list(word)
                if '/' in word1:
                    claimdoc= claimdoc
                if '(' in word1:
                    claimdoc = claimdoc
                elif ')' in word1:
                    claimdoc = claimdoc
                elif word =='(':
                    claimdoc+='-LRB-'
                elif word==')':
                    claimdoc+='-RRB-'
                elif word not in stoplist:
                        claimdoc +=word

            print(claimdoc)
            st_re=[]
            claim={}
            st_re=st1.tag(claimdoc.split())
            for re_pair in st_re:
                if re_pair[1] =='NNP' or re_pair[1]=='NN':
                    if re_pair[1] not in claim.keys():
                        claim[re_pair[1]]=re_pair[0]
                    else:
                        claim[re_pair[1]]=claim[re_pair[1]]+'_'+re_pair[0]
            #print(claim)
            total_re=[]
            for claim_re in claim.values():
                re_claim = searchFunction(claim_re)
                for re_re_claim in re_claim:
                    #print('re',re_re_claim)
                    if re_re_claim not in total_re:
                        total_re.append(re_re_claim)
            print('re',total_re)
            k=0
            for re in total_re:
                re_str=list(re)
                newClaim.write('\n\t' + '[' + '\n\t' + "\"" )
                if '\"' in re_str:
                    for re_re_str in re_str:
                        if re_re_str =='\"':
                            newClaim.write('\\"')
                        else:
                            newClaim.write(re_re_str)
                    if k == len(total_re) - 1:
                        newClaim.write("\"" + '\n\t' + ']' + '\n')
                    else:
                        newClaim.write( "\"" + '\n\t'+ '],' + '\n')
                        k += 1
                else:
                    if k == len(total_re) - 1:
                        newClaim.write(re + "\"" + '\n\t' + ']' + '\n')
                    else:
                        newClaim.write(re + "\"" + '\n\t'+ '],' + '\n')
                        k += 1
        # with open('./new_claim.json', 'a') as newClaim:
        #     #json.dump(total_claim, newClaim)
        #     newClaim.write('\n')
            l+=1
        newClaim.write("}")
del searcher
#newClaim.write("}")
newClaim.close()
trainset.close()
end = datetime.now()
print(end - start)