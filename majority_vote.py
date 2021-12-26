import os
import pandas as pd
from collections import defaultdict, Counter
from seqeval.metrics import f1_score

import re
#method to normalize character level missmatch such as ጸሀይ and ፀሐይ
def extract_sentences(docs, language=''):
    sentences = []
    sent = []
    n_sent = 0
    n_tokens = 0
    tags = []
    for i, line in enumerate(docs):
        if len(line) < 3:
            if len(sent) > 0:
                sentences.append(sent)
            sent = []
            n_sent += 1
        else:
            print(i, line)
            token, ne = line.strip().split('\t')
            sent.append((token, ne))

            tags.append(ne)
            n_tokens+=1

    print('# of sentences ', len(sentences))
    print('# of tokens ', n_tokens)

    return sentences

def take_to_bio_format(labels):
    bio_labels = []
    for k, label in enumerate(labels):
        ne = label
        if k > 0 and len(labels[k - 1]) > 2:
            prev_ne = labels[k - 1]
        else:
            prev_ne = 'O'
        new_ne = ne
        if new_ne != 'O':
            ne = 'B-' + new_ne
            if new_ne == prev_ne:
                ne = 'I-' + new_ne

        bio_labels.append(ne)

    return bio_labels

def export_ner_data(sentences, filename):
    all_sents = []
    n_tokens = 0
    tags = []

    with open(filename+'.txt', 'w') as f:
        for sent in sentences:
            labels = list(zip(*sent))[1]
            labels = take_to_bio_format(labels)
            words = list(zip(*sent))[0]
            sent = zip(words, labels)
            for token, tag in sent:
                f.write(token+" "+tag+"\n")
                all_sents.append([token, tag])
                n_tokens += 1
                if len(tag) > 2:
                    tags.append(tag[2:])
                else:
                    tags.append(tag)
            f.write("\n")
            all_sents.append(["", ""])

    #print(Counter(tags))

    print("#tokens ", n_tokens)
    #ner_df = pd.DataFrame(all_sents)
    #ner_df.to_csv(filename+'.tsv', sep="\t", header=None, index=None)


def majority_vote(filename, language='yoruba'):
    print(filename)
    with open(filename) as f:
        lines = f.read().splitlines()

    #with open('Annotations/conll_format/'+language+'.txt', 'w') as f:
    token_tags = []
    sel_tags = []
    for l, line in enumerate(lines):
        data_infos = line.strip().split('\t')
        if l==0: continue
        if len(data_infos) > 1:
            token, tags = data_infos[0], data_infos[1:]
            tag = max(tags,key=tags.count)
            token_tags.append(token+'\t'+tag)
            sel_tags.append(tag)
        else:
            token_tags.append('')

    sentences = extract_sentences(token_tags, language)

    sel_tags_dict = Counter(sel_tags)
    print(sum(sel_tags_dict.values()), sel_tags_dict)

    output_dir = 'data/labeled/naami_ner/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(sentences[0])

    N_sent = len(sentences)
    n_test = 310
    n_dev = 100
    test_sents = sentences[:n_test]
    dev_sents = sentences[n_test:n_test + n_dev]
    train_sents = sentences[n_test + n_dev:]

    print("all/test/valid/train split: ", N_sent, n_test, n_dev, N_sent - n_test - n_dev)
    all_splits = [train_sents, dev_sents, test_sents]

    for i, sents in enumerate(all_splits):
        if i == 0:
            filename = "train"
        elif i == 1:
            filename = "dev"
        else:
            filename = "test"

        export_ner_data(all_splits[i], output_dir+filename)


def extract_sentences_quality(filename, sep='\t', num_annotators=3):
    with open(filename) as f:
        docs = f.read().splitlines()

    sentences = []
    sent = []
    for i, line in enumerate(docs[1:]):
        if len(line) < 4:
            if len(sent) > 0:
                sentences.append(sent)
            sent = []
        else:
            #print(i, line)
            if num_annotators == 3:
                token, ne1, ne2, ne3 = line.strip().split(sep)
            else:
                token, ne1, ne2 = line.strip().split(sep)
                ne3='#~'

            sent.append((token, ne1, ne2, ne3))

    return sentences

def compute_inter_agreement(dir_name, lang):
    sentences = extract_sentences_quality(dir_name+lang+'.tsv', sep='\t', num_annotators=3)

    Label1, Label2, Label3 = [], [], []
    for sent in sentences:
        labels1 = list(zip(*sent))[1]
        labels1 = take_to_bio_format(labels1)
        Label1.append(labels1)

        labels2 = list(zip(*sent))[2]
        labels2 = take_to_bio_format(labels2)
        Label2.append(labels2)

        labels3 = list(zip(*sent))[3]
        labels3 = take_to_bio_format(labels3)
        Label3.append(labels3)

    print('Inter-agreement (G1, G2): ', f1_score(Label1, Label2))
    print('Inter-agreement (G1, G3): ', f1_score(Label1, Label3))
    print('Inter-agreement (G2, G3): ', f1_score(Label2, Label3))





if __name__ == '__main__':
    majority_vote('data/ioAnnotator_tsv/ne/ne.tsv', 'ne')
    compute_inter_agreement('data/ioAnnotator_tsv/ne/', 'ne')


