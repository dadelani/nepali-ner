import spacy
from spacy.pipeline.sentencizer import Sentencizer

# Stemmer adapted from Singh et. al.
# https://github.com/oya163/nepali-ner
from stemmer import NepStemmer

# Load Nepali nlp model
nlp = spacy.blank("ne")

# Set up punctuation for sentence
custom_puncts = Sentencizer.default_punct_chars
# Nepali doesn't use period as sentence demarcation, so we can remove it
custom_puncts.remove(".")

# Add sentence tokenizer to nlp model
nlp.add_pipe("sentencizer", config={"punct_chars": custom_puncts})

# Initialize Stemmer
nepstem = NepStemmer()

def tokenize_sent(text):
	"""
	Takes a text corpus and converts it to a list of sentences

	:param text: str - the text corpus (in Devanagari script)
	:returns: List(str) - list of sentences
	"""
	text = nlp(text)
	sentences = [str(sent) for sent in text.sents]
	return sentences

def tokenize(text, stem=False):
	"""
	Takes a text corpus and converts it to a list of tokens (words or word roots + suffixes)

	:param text: str - the text corpus (in Devanagari script)
	:param stem: bool - if True returns stemmed tokens
	:returns: List(str) - list of tokens (words or word roots + suffixes)
	"""
	if stem:
		text = nepstem.stem(text)

	text = nlp(text)
	tokens = [str(token) for token in text]

	return tokens



