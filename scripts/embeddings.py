#!/usr/bin/env python3

"""
Reads keyed vectors in word2vec format.
Fallbacks to <unk> embedding if word is not present. 
"""

from flair.embeddings import TokenEmbeddings
from flair.data import Sentence
from typing import List
from gensim.models import KeyedVectors
import torch
import numpy as np

class KeyedWordEmbeddings(TokenEmbeddings):
    def __init__(self, embeddings):
        self.name = embeddings
        self.static_embeddings = True
        self.precomputed_word_embeddings = KeyedVectors.load_word2vec_format(embeddings)
        self.known_words = set(self.precomputed_word_embeddings.index2word)
        self.__embedding_length: int = self.precomputed_word_embeddings.vector_size
        super().__init__()

    @property
    def embedding_length(self) -> int:
        return self.__embedding_length

    def _add_embeddings_internal(self, sentences: List[Sentence]) -> List[Sentence]:
        for i, sentence in enumerate(sentences):
            for token, token_idx in zip(sentence.tokens, range(len(sentence.tokens))):
                token: Token = token
                if token.text in self.known_words:
                    word_embedding = self.precomputed_word_embeddings[token.text]
                elif token.text.lower() in self.known_words:
                    word_embedding = self.precomputed_word_embeddings[token.text.lower()]
                else:
                    word_embedding = self.precomputed_word_embeddings['<unk>']
                word_embedding = torch.FloatTensor(word_embedding)
                token.set_embedding(self.name, word_embedding)
        return sentences
