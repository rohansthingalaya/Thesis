from __future__ import print_function
import spacy
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
import PyPDF2
import re
import pandas as pd
from io import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


nlp = spacy.load('en_core_web_sm')
phrasematcher = PhraseMatcher(nlp.vocab)
matcher = Matcher(nlp.vocab)


myfile = open('evaluation.pdf', mode = 'rb')
pdf_text = []
pdf_reader = PyPDF2.PdfFileReader(myfile)
for p in range(pdf_reader.numPages):
    page = pdf_reader.getPage(p)
    pdf_text.append(page.extractText())
myfile.close()

list1 = pdf_text
str1 = ''.join(list1)
doc = nlp(str1)


matched_sents = []

def P_sents(phrasematcher, doc, i, pmatches, label = 'MATCH'):
    match_id, start, end = pmatches[i]
    span = doc[start : end]
    sent = span.sent

    if doc.vocab.strings[match_id] == 'computation':
        match_ents = 'computation'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'data_defination':
        match_ents = 'data_defination'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'process':
        match_ents = 'process'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'constraint':
        match_ents = 'constraint'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'assumption':
        match_ents = 'assumption'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'model':
        match_ents = 'model'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'performance':
        match_ents = 'performance'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'hardware':
        match_ents = 'hardware'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })


def m_sents(matcher, doc, i, matches, label = 'MATCH'):
    match_id, start, end = matches[i]
    span = doc[start : end]
    sent = span.sent

    if doc.vocab.strings[match_id] == 'Pattern1':
        match_ents = 'Pattern1'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'Pattern2':
        match_ents = 'Pattern2'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'Pattern3':
        match_ents ='Pattern3'
        #matched_sents.append(sent.text)
        matched_sents.append({'Requirement candidate': sent.text, 'ents' : match_ents})

computation = ['method', 'technique', 'approach', 'algorithm']
data_defination = ['data','information','file','format']
process = ['process','calculate','compute','discretize', 'input', 'output']
constraint = ['constraint','restriction', 'restraint', 'limitation']
assumption = ['assume','assumption', 'hypothesis']
model = ['model','framework']
performance = ['efficient','speed', 'robust']
hardware = ['CPU','memory']

phrasematcher.add('computation', P_sents, *[nlp(text) for text in computation])
phrasematcher.add('datadefination', P_sents, *[nlp(text) for text in data_defination])
phrasematcher.add('process', P_sents, *[nlp(text) for text in process])
phrasematcher.add('constraint', P_sents, *[nlp(text) for text in constraint])
phrasematcher.add('assumption', P_sents, *[nlp(text) for text in assumption])
phrasematcher.add('model', P_sents, *[nlp(text) for text in model])
phrasematcher.add('performance', P_sents, *[nlp(text) for text in performance])
phrasematcher.add('hardware', P_sents, *[nlp(text) for text in hardware])

#pattern1 = [{'LOWER' : 'shant'}]
pattern2 = [{'POS': 'NOUN'}, {'POS': 'VERB', 'TAG' : 'MD'}]
pattern3 = [{'POS': 'NOUN'}, {'POS': 'VERB', 'TAG' : 'VBZ'}]


#matcher.add('Pattern1', m_sents, pattern1)  
matcher.add('Pattern2', m_sents, pattern2)
matcher.add('Pattern3', m_sents, pattern3)


pmatches = phrasematcher(doc)
matches = matcher(doc)

df = pd.DataFrame(matched_sents)
for row in df.loc[:,"Requirement candidate"]:
    df = df.replace('\n','', regex=True)

cv = CountVectorizer(max_df=0.9,min_df=2,stop_words='english')
dtm = cv.fit_transform(df['Requirement candidate'])
LDA = LatentDirichletAllocation(n_components=5,random_state=42)
LDA.fit(dtm)
#single_topic = LDA.components_[0]
#top_twenty_words = single_topic.argsort()[-10:]
topic_results = LDA.transform(dtm)
df['Topic'] = topic_results.argmax(axis=1)
df.to_csv('output1.csv')
