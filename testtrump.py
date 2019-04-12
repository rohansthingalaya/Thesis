from __future__ import print_function
import spacy
from spacy.matcher import Matcher
from spacy import displacy
import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import seaborn as sns
nlp = spacy.load('en_core_web_sm')

#tweets = pd.read_csv("C:\\Users\\Rohan\\Desktop\\python\\Thesis\\all_djt_tweets.csv", dtype='unicode')
#text = tweets['text'].str.cat(sep=' ')
#max_length = 1000000-1
#text = text[:max_length]
#retext = text.str.cat(sep='')
#text = (u'I am pleased  to announce that, effective 4/9/18, @AmbJohnBolton will be my new National Security Advisor.If Democrats were not such obstructionists and understood the power of lower taxes, we would be able to get many of their ideas into Bill!We’re getting close! We shall do it. I am truly honored  and grateful for receiving SO much support from our American Crooked Hillarys V pick said this morning that I was not aware that Russia took over Crimea.')
#doc = nlp(text)
with open('C:\\Users\\Rohan\\Desktop\\python\\Thesis\\twitter.txt') as f:
    doc = nlp(f.read())
matcher = Matcher(nlp.vocab)
matched_sents = []

def collect_sents(matcher, doc, i, matches, label = 'MATCH'):
    match_id, start, end = matches[i]
    span = doc[start : end]
    sent = span.sent

    if doc.vocab.strings[match_id] == 'DEMOCRATS':  
        #match_ents = [{'start': span.start_char - sent.start_char,
                   #'end': span.end_char - sent.start_char,
                   #'label': 'DEMOCRATS'}]
        match_ents = [{'labels' : 'DEMOCRATS'}]
        matched_sents.append({'text': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'RUSSIA':  
        #match_ents = [{'start': span.start_char - sent.start_char,
               #'end': span.end_char - sent.start_char,
               #'label': 'RUSSIA'}]
        match_ents = [{'labels' : 'RUSSIA'}]
        matched_sents.append({'text': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'I':  
        #match_ents = [{'start': span.start_char - sent.start_char,
               #'end': span.end_char - sent.start_char,
               #'label': 'NARC'}]
        match_ents = [{'labels' : 'NARC'}]
        matched_sents.append({'text': sent.text, 'ents': match_ents })

russia_pattern = [{'LOWER': 'russia'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]
democrats_pattern = [{'LOWER': 'democrats'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]
#i_pattern = [{'LOWER': 'I'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
           #{'POS': 'ADJ'}]
#matcher = Matcher(nlp.vocab)
matcher.add('DEMOCRATS', collect_sents, democrats_pattern)  # add pattern
matcher.add('RUSSIA', collect_sents, russia_pattern)  # add pattern
#matcher.add('I', collect_sents, i_pattern)  # add pattern

matches = matcher(doc)
#print(matches)

print(matched_sents)
#matched_sents
#spacy.displacy.render(matched_sents, style='ent', manual=True, options = {'colors': {'NARC': '#6290c8', 'RUSSIA': '#cc2936', 'DEMOCRATS':'#f2cd5d'}})


