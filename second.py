import spacy
from spacy.matcher import PhraseMatcher

patterns = {'HelloWorld': [{'LOWER': 'hello'}, {'LOWER': 'world'}]}
matcher = PhraseMatcher(nlp.vocab)