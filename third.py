import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')


def on_match(matcher, doc, id, matches):
    print('Matched!', matches)
    

matcher = Matcher(nlp.vocab)
matcher.add('HelloWorld', on_match, [{'LOWER': 'hello'}, {'LOWER': 'world'}])
matcher.add('GoogleMaps', on_match, [{'ORTH': 'Google'}, {'ORTH': 'Maps'}])
doc = nlp(u'HELLO WORLD on Google Maps.')
matches = matcher(doc)