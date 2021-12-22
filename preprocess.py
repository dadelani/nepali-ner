import os


def create_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def export_to_conll(sentences, output_path):
    with open(output_path, 'w') as f:
        for sent in sentences:
            for word, tag in sent:
                f.write(word+' '+tag+'\n')
            f.write('\n')


def extract_ner_sentences(filename, sep='\t', domain='wiki'):
    with open(filename) as f:
        docs = f.read().splitlines()

    sentences = []
    sent = []
    tags = []
    for i, line in enumerate(docs):
        if len(line) < 3:
            if len(sent) > 0:
                sentences.append(sent)
            sent = []
        else:
            #print(i, line)
            token, ne = line.strip().split(sep)
            if ne.endswith('MISC') or ne.endswith('DATE'):
                ne = 'O'
            if domain=='wiki':
               token = token[3:]

            sent.append((token, ne))

            tags.append(ne)
    print(filename, '# of sentences ', len(sentences))

    return sentences

def preprocess_wikiann(lang='ne'):
    dir_name = 'data/downloaded/wikiann_'+lang+'/'
    train_sentences = extract_ner_sentences(dir_name + 'train')
    dev_sentences = extract_ner_sentences(dir_name + 'dev')
    test_sentences = extract_ner_sentences(dir_name + 'test')

    print(len(train_sentences), len(dev_sentences), len(test_sentences))

    output_dir = 'data/labeled/wikiann_'+lang+'/'
    create_dir(output_dir)

    export_to_conll(train_sentences, output_dir + 'train.txt')
    export_to_conll(dev_sentences, output_dir + 'dev.txt')
    export_to_conll(test_sentences, output_dir + 'test.txt')

def preprocess_nepali_dataset():
    dir_name = 'data/downloaded/'
    sentences = extract_ner_sentences(dir_name + 'total.bio.txt', domain='news')

    N = len(sentences)
    n_train = int(N * 0.7)
    n_dev = int(N * 0.8)

    output_dir = 'data/labeled/singh_ner/'
    create_dir(output_dir)

    train_sentences = sentences[:n_train]
    dev_sentences = sentences[n_train:n_dev]
    test_sentences = sentences[n_dev:]

    print(len(train_sentences), len(dev_sentences), len(test_sentences))
    export_to_conll(train_sentences, output_dir + 'train.txt')
    export_to_conll(dev_sentences, output_dir + 'dev.txt')
    export_to_conll(test_sentences, output_dir + 'test.txt')

if __name__ == '__main__':
    preprocess_wikiann(lang='ne')
    preprocess_wikiann(lang='hi')
    preprocess_nepali_dataset()

