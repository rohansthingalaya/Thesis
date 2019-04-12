from __future__ import print_function
from spacy.tokenizer import Tokenizer
import spacy
from spacy.matcher import Matcher
import PyPDF2
nlp = spacy.load('en_core_web_sm')

matcher = Matcher(nlp.vocab)

with open ('Horizon.pdf', mode = 'rb') as pdf_file, open('sample.txt', 'w') as text_file:
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    for page_number in range(number_of_pages):
        page = read_pdf.getPage(page_number)
        page_content = page.extractText()
        text_file.write(page_content)
with open ('sample.txt') as f:
    doc = nlp(f.read())

matched_sents = []


#for num, sentence in enumerate(doc.sents):
    #print(f'{num}: {sentence}')

#for token in doc:
    #print(token.text, token.pos_, token.tag_, token.lemma_ )
def m_sents(matcher, doc, i, matches, label = 'MATCH'):
    match_id, start, end = matches[i]
    span = doc[start : end]
    sent = span.sent

    if doc.vocab.strings[match_id] == 'Pattern1':
        match_ents = [{'label': 'Pattern1'}]
        matched_sents.append({'text': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'Pattern2':
        match_ents = [{'label': 'Pattern2'}]
        matched_sents.append({'text': sent.text, 'ents': match_ents })
    elif doc.vocab.strings[match_id] == 'Pattern3':
        match_ents =[{'Label' : 'Pattern3'}]
        matched_sents.append({'text' : sent.text, 'ents' : match_ents})

        
#pattern1 = [{'LOWER' : 'must'}]
pattern2 = [{'POS': 'NOUN'}, {'POS': 'VERB', 'TAG' : 'MD'}]
pattern3 = [{'POS': 'NOUN'}, {'POS': 'VERB', 'TAG' : 'VBZ'}]

#matcher.add('Pattern1', m_sents, pattern1)  
matcher.add('Pattern2', m_sents, pattern2)
matcher.add('Pattern3', m_sents, pattern3)

matches = matcher(doc)
#print(matched_sents)
for num, sentence in enumerate(matched_sents):
    print(f'{num}: {sentence}')
