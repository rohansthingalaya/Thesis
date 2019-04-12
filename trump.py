import spacy
from spacy.matcher import Matcher
import pandas as pd
import re
import csv
nlp = spacy.load('en_core_web_sm')
tweets = pd.read_csv("C:\\Users\\Rohan\\Desktop\\python\\Thesis\\all_djt_tweets.csv", dtype='unicode')

#one_sentence = tweets['text'][300]
#doc = nlp(one_sentence)
#spacy.displacy.render(doc, style='ent')

#for token in doc:
    #print(token, token.pos_)
text = tweets['text'].str.cat(sep='')
max_length = 1000000-1
text = text[:max_length]

url_reg  = r'[a-z]*[:.]+\S+'
text   = re.sub(url_reg, '', text)
noise_reg = r'\&amp'
text   = re.sub(noise_reg, '', text)

doc = nlp(text)


matcher = Matcher(nlp.vocab)
matched_sents = []


def collect_sents(matcher, doc, i, matches, label='MATCH'):
    match_id, start, end = matches[i]
    span = doc[start : end]
    sent = span.sent

    if doc.vocab.strings[match_id] == 'DEMOCRATS':
        match_ents = [{'start': span.start_char - sent.start_char,
                   'end': span.end_char - sent.start_char,
                   'label': 'DEMOCRATS'}]
        matched_sents.append({'text' : sent.text, 'ents' : match_ents})
    
    elif doc.vocab.strings[match_id] == 'Russia' :
        match_ents = [{'start': span.start_char - sent.start_char,
               'end': span.end_char - sent.start_char,
               'label': 'RUSSIA'}]
        matched_sents.append({'text' : sent.text, 'ents' : match_ents})

    elif doc.vocab.strings[match_id] == 'I' :
        match_ents = [{'start': span.start_char - sent.start_char,
               'end': span.end_char - sent.start_char,
               'label': 'NARC'}]
        matched_sents.append({'text' : sent.text, 'ents' : match_ents})

russia_pattern = [{'LOWER' : 'russia'}, {'Lemma' : 'be'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]
democrats_pattern = [{'LOWER': 'democrats'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]
i_pattern = [{'LOWER': 'i'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]

matcher.add('DEMOCRATS', collect_sents, democrats_pattern)
matcher.add('RUSSIA', collect_sents, russia_pattern)
matcher.add('I', collect_sents, i_pattern)
matches = matcher(doc)

spacy.displacy.render(matched_sents, style='ent', manual=True, options= {'colors' : {'NARC': '#6290c8', 'RUSSIA': '#cc2936', 'DEMOCRATS':'#f2cd5d'}})
