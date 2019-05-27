#named entities recognization
import nltk
#import stanfordner

from nltk import StanfordNERTagger
#nltk.download('StanfordNERTagger')
jar='/Users/agatha/anaconda3/lib/python3.7/site-packages/stanford-ner-2018-10-16/stanford-ner.jar'
#model =

st = StanfordNERTagger(model_filename='/Users/agatha/anaconda3/lib/python3.7/site-packages/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',path_to_jar=jar)
print(st.tag('Rami Eid is studying at Stony Brook University in NY'.split()))

