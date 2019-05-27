import re
from allennlp.predictors import Predictor
valid_annotations_pre = '[B|I|U|L]-|PERSON|NORP|FAC|ORG|GPE|LOC|PRODUCT|EVENT|WORK_OF_ART|LAW|LANGUAGE'
predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/fine-grained-ner-model-elmo-2018.12.21.tar.gz")

def get_useful_words(ner_result):
    word_list ={}
    phrase = ''
    for word,tag in zip(ner_result['words'],ner_result['tags']):
        tag_list=list(tag)
        if '-' in tag_list:
            tag =tag.split('-')
            if bool(re.match(valid_annotations_pre,tag[1])):
                if tag[1] not in word_list.keys():
                    word_list[tag[1]]=[]
                    if 'U' in tag[0]:
                        word_list[tag[1]].append(word)
                    elif 'B' in tag[0]:
                        phrase = word
                    elif 'I' in tag[0]:
                        phrase+='_'+word
                    elif 'L' in tag[0]:
                        phrase +='_'+word
                        word_list[tag[1]].append(phrase)
                        phrase = ''
                else:
                    if 'U' in tag[0]:
                        word_list[tag[1]].append(word)
                    elif 'B' in tag[0]:
                        phrase = word
                    elif 'I' in tag[0]:
                        phrase+='_'+word
                    elif 'L' in tag[0]:
                        phrase +='_'+word
                        word_list[tag[1]].append(phrase)
                        phrase = ''
    return word_list


allen_re = predictor.predict(sentence='Noah Cyrus is a younger sister of Macy Grey')
print(allen_re['tags'])
wordlist= get_useful_words(allen_re)
print(wordlist)