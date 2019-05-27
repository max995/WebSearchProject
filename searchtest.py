#### need to deal with claim


import lucene
from datetime import datetime
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from pip._vendor.distlib.compat import raw_input
from java.io import File
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer

lucene.initVM()

searcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File("./index/").toPath())))
analyzer = StandardAnalyzer()
print('query','Savages')
query = QueryParser("docName", analyzer).parse('Tatum_ONeal')
#query1 =QueryParser("content",analyzer).parse('wa_born_in_a_hospital_')
scoreDocs = searcher.search(query,3).scoreDocs
#scoreDocs1=searcher.search(query1,2000).scoreDocs
print ("%s total matching documents." % len(scoreDocs))
results = []
#print(scoreDocs)
start = datetime.now()
for scoreDoc in scoreDocs:
    #for scoreDoc1 in scoreDocs1:
    print(scoreDoc)
    doc = searcher.doc(scoreDoc.doc)
    #doc1 = searcher.doc1(scoreDoc1.doc1)
    print("name", doc.get("name"),
          "line", doc.get("line"),
          "docName", doc.get("docName"),
          "content",doc.get("content"))
       #"content",doc.get("content"))
# for listpair in results:
#     if doc
    #if doc.get("docName")==doc1.get("docName"):
    wp=[]
    if doc.get("docName") not in results:
        wp = list(doc.get("docName"))
        print(wp)

        if '\"' not in wp:
            results.append(doc.get("docName"))
        elif '\"' in wp:
            for n in wp:
                if n=='\"':
                    n='\\"'
            print(wp)
        results.append([doc.get("docName").replace('"','\"')])
print(results)

del searcher
end = datetime.now()
print(end - start)