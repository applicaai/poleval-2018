#!/usr/bin/env python3

"""
Functions utilized to read data sets in our internal format
and store them as flair BIO-tagged corpora.
"""

from typing import List
from flair.data import Sentence, TaggedCorpus, Token

def data_to_bio(labels_data, text, entities):
    tokens = text.split()
    labels = ['O'] * len(tokens)
    for single in labels_data.split():
        single = single.split(':')
        if single[0] not in entities:
            continue
        ids = single[1].split(',')
        for x, id in enumerate(ids):
            pref = 'I-'
            if x == 0:
                pref = 'B-'
            labels[int(id)-1] = f'{pref}{single[0]}'
    return labels, tokens

def read_group_file(path_to_file, entities):
    sentences: List[Sentence] = []
    for line in open(path_to_file):
        sentence: Sentence = Sentence()
        labels_data, text = line.rstrip().split('\t')
        labels, tokens = data_to_bio(labels_data, text, entities)
        for label, token in zip(labels, tokens):
            token = Token(token)
            token.add_tag('ner', label)
            sentence.add_token(token)
        sentences.append(sentence)
    return sentences

def read_group(entities):
    sentences_dev = read_group_file('data/dev.tsv', entities)
    sentences_train = read_group_file('data/train.tsv', entities)
    return TaggedCorpus(sentences_train, sentences_dev, sentences_dev)
