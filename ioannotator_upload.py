import os

import requests
import csv
import xmltodict
import pandas as pd
from nltk.tokenize import word_tokenize

# get your API key https://app.ioannotator.com/api
params = {'apikey': ''}
api = 'https://api.ioannotator.com/import/texts'


def extract_token_sentences(filename):
    with open(filename) as f:
        docs = f.read().splitlines()

    sentences = []
    sent = []
    for i, line in enumerate(docs):
        if len(line) < 1:
            if len(sent) > 0:
                sentences.append(' '.join(sent))
            sent = []
        else:
            sent.append(line.strip())

    print(filename, '# of sentences ', len(sentences))

    return sentences


def upload_language_document(dir_name, lang, dataset_ids, tokenized=False):

    if tokenized:
        sentences = extract_token_sentences(dir_name)
    else:
        with open(dir_name, 'r') as f:
            sentences = f.read().splitlines()

    for d_id in dataset_ids:
        for s, row in enumerate(sentences):
            words = word_tokenize(row)
            row = ' '.join(words)
            print(row)
            data = {
                'dataset': d_id,
                'text': row,
                'reference': s+1,
            }
            x = requests.post(api, json=data, params=params)
            print(s, x)
        print("\n")


def get_label_dict():
    label_dict = [('PER','P'),('ORG','O'),('LOC','L')]
    label_dict = dict(label_dict)

    print(len(label_dict), label_dict)

    return label_dict

def add_labels(labels_dict, lang, dataset_ids):

    for d_id in dataset_ids:
        for category, shortcut in labels_dict.items():
            payload = {
                "name": category,
                "dataset": d_id,
                "key": shortcut
            }

            r = requests.post("https://api.ioannotator.com/label?apikey="+params['apikey'], json=payload)
            print(d_id, r)




if __name__ == '__main__':
    dir_name = 'data/unlabeled/eng.txt'
    label_dict = get_label_dict()
    upload_language_document(dir_name, 'eng', ['5703869787013120'])
    add_labels(label_dict, 'eng', ['5703869787013120'])

    dir_name = 'data/unlabeled/nepali_ner_stemmed_corpus_final.txt'
    #upload_language_document(dir_name, 'nep', ['5736615892746240'], tokenized=True)
    #add_labels(label_dict, 'eng', ['5718945860419584', '5151827171475456', '5734642221056000'])
    #upload_language_document(dir_name, 'nep', ['5718945860419584', '5151827171475456', '5734642221056000'], tokenized=True)
