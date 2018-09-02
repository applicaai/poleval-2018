#!/usr/bin/env python3

"""
Forward and backward character-level language models were trained on 1B words corpus
of Polish composed in one third of respectively subsamples from: Polish Wikipedia,
PolEval's language modeling task (supposably the National Corpus of Polish) and
Polish Common Crawl.

We used exactly the same parameters, setting and assumptions as Akbik et. al (2018),
achieving the final perplexity of 2.41 for forward and 2.46 for backward LM.

GloVe embeddings were trained on a whole Common Crawl-based Web corpus of Polish
for all the tokens present in PolEval task's corpora (symmetric, cased, 300 dimensions,
30 iterations, window size of 15).
"""

from flair.file_utils import cached_path

ROOT_URL = 'https://s3.eu-central-1.amazonaws.com/borchmann'
FORWARD_FILE = 'cse/lm-polish-forward-v0.2.pt'
BACKWARD_FILE = 'cse/lm-polish-backward-v0.2.pt'
GLOVE_FILE = 'glove/poleval.txt'

FORWARD_LM = cached_path(f'{ROOT_URL}/{FORWARD_FILE}', cache_dir='models')
BACKWARD_LM = cached_path(f'{ROOT_URL}/{BACKWARD_FILE}', cache_dir='models')
GLOVE = cached_path(f'{ROOT_URL}/{GLOVE_FILE}', cache_dir='models')
