from __future__ import print_function
import spacy
from spacy.matcher import Matcher
from spacy import displacy
import pandas as pd
import re
import csv
from io import StringIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

nlp = spacy.load('en_core_web_sm')

with open('papermade.txt') as f:
    doc = nlp(f.read())
matcher = Matcher(nlp.vocab)
matched_sents = []

def collect_sents(matcher, doc, i, matches, label = 'MATCH'):
    match_id, start, end = matches[i]
    span = doc[start : end]
    sent = span.sent

    if doc.vocab.strings[match_id] == 'RUSSIA': 
        match_ents = [{'start': span.start_char - sent.start_char,
                   'end': span.end_char - sent.start_char,
                   'label': 'RUSSIA'}]
        matched_sents.append(sent.text)
    #if doc.vocab.strings[match_id] == 'ROME': 
        #match_ents = [{'start': span.start_char - sent.start_char,
                   #'end': span.end_char - sent.start_char,
                   #'label': 'ROME'}]
        #matched_sents.append({'text': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'DEMOCRATS':
        match_ents = [{'start': span.start_char - sent.start_char,
               'end': span.end_char - sent.start_char,
               'label': 'DEMOCRATS'}]
        matched_sents.append(sent.text)       
        #matched_sents.append({'text': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'I':
        match_ents = [{'start': span.start_char - sent.start_char,
               'end': span.end_char - sent.start_char,
               'label': 'NARC'}]
        matched_sents.append(sent.text)
        #matched_sents.append({'text': sent.text, 'ents': match_ents })


#words = ['data', 'should']
#wordlist = [nlp(text) for text in words]


russia_pattern = [{'LOWER' : 'must'}]
rome_pattern = [{'LOWER' : 'should'}]
#data_pattern = [{'LOWER' : 'data'}]
#democrats_pattern = [{'POS':'DET'},{'POS': 'NOUN'}, {'LEMMA': 'should'}, {'POS': 'ADV', 'OP': '*'},
           #{'POS': 'ADJ'}]
i_pattern = [{'POS': 'NOUN'}, {'LEMMA': 'may'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]

#add patterns
#matcher.add('DEMOCRATS', collect_sents, democrats_pattern)
#matcher.add('DEMOCRATS', collect_sents, *wordlist)
matcher.add('RUSSIA', collect_sents, russia_pattern, rome_pattern )  
#matcher.add('ROME', collect_sents, rome_pattern)
matcher.add('I', collect_sents, i_pattern)  

matches = matcher(doc)
#print(matched_sents)
#or num, sentence in enumerate(matched_sents):
    #print(f'{num}: {sentence}')

list2 = matched_sents
str2 = ''.join(list2)

npr = pd.read_csv(StringIO(str2))
#print(npr)
cv = CountVectorizer(max_df=0.9,min_df=2,stop_words='english')

dtm = cv.fit_transform(npr)

LDA = LatentDirichletAllocation(n_components=3,random_state=42)
LDA.fit(dtm)