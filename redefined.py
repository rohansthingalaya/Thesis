from __future__ import print_function
import spacy
from spacy.matcher import Matcher
import re
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

russia_pattern = [{'LOWER' : 'should'}]
democrats_pattern = [{'POS': 'NOUN'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]
i_pattern = [{'POS': 'PRON'}, {'LEMMA': 'be'}, {'POS': 'ADV', 'OP': '*'},
           {'POS': 'ADJ'}]

matcher.add('Test pattern',None, russia_pattern, democrats_pattern, i_pattern)
with open('C:\\Users\\Rohan\\Desktop\\python\\Thesis\\rupps.txt') as f:
    doc = nlp(f.read())

#sentences = [sent.string.strip() for sent in doc.sents]
#print(sentences)
#doc = nlp(u"I am pleased  to announce that, effective 4/9/18, @AmbJohnBolton will be my new National Security Advisor.If Democrats were not such obstructionists and understood the power of lower taxes, we would be able to get many of their ideas into Bill!We’re getting close! We shall do it. I am truly honored  and grateful for receiving SO much support from our American Crooked Hillarys V pick said this morning that I was not aware that Russia took over Crimea.")
found_matches = matcher(doc)
#print(found_matches)

for match_id, start, end in found_matches:
    string_id = nlp.vocab.strings[match_id]
    span = doc[start:end]
    print(match_id, string_id, start, end, span.text)