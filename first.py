from __future__ import print_function
from spacy.tokenizer import Tokenizer
import spacy
nlp = spacy.load('en_core_web_sm')

tokenizer = Tokenizer(nlp.vocab)
#doc_file = nlp(open("madeup.txt").read())
#doc = nlp('Indirect eligible costs are calculated as a flat rate of 25% of direct eligible costs')
doc = nlp('The eligible costs of coordination and networking activities may not exceed 30% of the total estimated eligible costs set up in the budget of the action at the signature of the grant agreement.')

#for token in doc_file:
    #print(token.text)
#for num, sentence in enumerate(doc_file.sents):

for num, sentence in enumerate(doc.sents):
    print(f'{num}: {sentence}')

#for token in doc_file:
    #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
 
          #token.shape_, token.is_alpha, token.is_stop)
for token in doc:
    print(token.text, token.pos_, token.tag_, token.lemma_ )
#print(doc_file)
#with open ('insur.txt') as fin:
    #for line in fin:
        #tokens = tokenizer.tokenizer(line)
        #print(''.join(tokens), end='\n')
