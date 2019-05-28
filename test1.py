
import os
import lucene
from datetime import datetime
from java.io import File
from org.apache.lucene.document import Document, Field, StoredField, StringField, TextField
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo,IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory


start = datetime.now()
lucene.initVM()
indexDir = SimpleFSDirectory(File("./index/").toPath())
analyzer = StandardAnalyzer()
# writeConfig = IndexWriterConfig(lucene.VERSION,StandardAnalyzer())
writeConfig = IndexWriterConfig(analyzer)
writer = IndexWriter(indexDir, writeConfig)
root ="./Data/wiki-pages-text"

t1 = FieldType()

t1.setStored(True)
t1.setTokenized(False)
t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)



t3 = FieldType()

t3.setStored(True)# no saving
t3.setTokenized(True)##no need to
t3.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)



for root, dirnames, filenames in os.walk(top=root):
    print(len(filenames))
    for filename in filenames:
        if not filename.endswith('.txt'):
            continue
        print("adding", filename)
        path = os.path.join(root, filename)
        file = open(path)
        contents = open(path, encoding="utf8")
        i = 0
        # contents = file.read()
        while True:
            #file.seek(i)
            line = file.readline()
            doc = Document()
            if not line:
                break
            docName = line.split()[0]
            docIndex= line.split()[1]
            doc.add(Field("name", filename , t1))
            #doc.add(Field("index",docIndex,t1))
            doc.add(Field("line", str(i),t1))
            doc.add(Field("docName",docName, t3))
            doc.add(Field("content",line.replace(docName,''),t3))
            #print(doc)
            writer.addDocument(doc)
            i+=1
        file.close()
    #filename.close()
#ticker = Ticker()
writer.commit()
writer.close()

end = datetime.now()
print(end - start)


