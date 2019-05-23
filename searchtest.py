####？？？？？

import lucene

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
#while True:
    #command = raw_input("Query:")
query = QueryParser("content", analyzer).parse("Nikolaj Coster-Waldau worked with the Fox Broadcasting Company")
scoreDocs = searcher.search(query,2000).scoreDocs
print ("%s total matching documents." % len(scoreDocs))
results = []
#print(scoreDocs)
for scoreDoc in scoreDocs:
    #print(scoreDoc)
    doc = searcher.doc(scoreDoc.doc)
    # print(doc)
    print("name", doc.get("name"),
          "docName", doc.get("docName"))
          # "content",doc.get("content"))
    # for listpair in results:
    #     if doc
    results.append([doc.get("name"),doc.get("docName")])
#print(results)

del searcher