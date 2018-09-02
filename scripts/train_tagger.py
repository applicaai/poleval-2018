#!/usr/bin/env python3

"""
Trains per-group sequence tagging models, that is LSTM-CRFs with one bidirectional
LSTM layer and 512 hidden states on 300-dimensional GloVe embeddings,
as well as embeddings from forward and backward LMs with 2048 hidden states.
"""

from typing import List
from flair.embeddings import StackedEmbeddings, CharLMEmbeddings, TokenEmbeddings
from flair.models import SequenceTagger
from flair.trainers import SequenceTaggerTrainer
from flair.data import TaggedCorpus

from models import FORWARD_LM, BACKWARD_LM, GLOVE
from embeddings import KeyedWordEmbeddings
from ne_groups import GROUPS
from corpora import read_group

embedding_types: List[TokenEmbeddings] = [
    KeyedWordEmbeddings(GLOVE),
    CharLMEmbeddings(FORWARD_LM),
    CharLMEmbeddings(BACKWARD_LM)
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

for entities in GROUPS:
    corpus: TaggedCorpus = read_group(entities)
    tag_dictionary = corpus.make_tag_dictionary(tag_type='ner')
    tagger: SequenceTagger = SequenceTagger(hidden_size=512,
                                            embeddings=embeddings,
                                            tag_dictionary=tag_dictionary,
                                            tag_type='ner',
                                            use_crf=True)
    trainer: SequenceTaggerTrainer = SequenceTaggerTrainer(tagger, corpus, test_mode=True)
    file_name = '-'.join(entities)
    trainer.train(f'data/models/{file_name}',
                   learning_rate=0.05,
                   mini_batch_size=124,
                   max_epochs=40,
                   save_model=True)
