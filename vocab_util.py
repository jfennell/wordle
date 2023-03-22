import collections
import os.path

from typing import Dict


VOCAB_DIR = 'vocab-data/'
WORDS_ALPHA_VOCAB = 'words_alpha.txt'
UNIGRAM_FREQ_VOCAB = 'unigram_freq.csv'
DERIVED_VOCAB = 'derived.csv'

def get_txt_vocab(path):
    with open(path) as f:
        vocab = {w.strip():1 for w in f.read().split()}
    return vocab

def get_weighted_vocab(path):
    vocab = {}
    with open(path) as f:
        for l in f.read().split():
            w, c = l.split(',', 2)
            vocab[w] = int(c)
    return vocab

_loader_config = {
        WORDS_ALPHA_VOCAB: dict( 
            path=os.path.join(VOCAB_DIR, WORDS_ALPHA_VOCAB),
            loader=get_txt_vocab,
        ),
        UNIGRAM_FREQ_VOCAB: dict(
            path=os.path.join(VOCAB_DIR, UNIGRAM_FREQ_VOCAB),
            loader=get_weighted_vocab,
        ),
        DERIVED_VOCAB: dict(
            path=os.path.join(VOCAB_DIR, DERIVED_VOCAB),
            loader=get_weighted_vocab,
        ),
}
class UnknownVocabException(Exception):
    pass

class VocabLoader():
    def __init__(self, config=_loader_config):
        self.config = dict(config)
        self.cache =  {}

    def load(self, vocab_name, memoize=True):
        if vocab_name not in self.config:
            raise UnknownVocabException(f'Did not recognize "{vocab_name}"')

        if memoize and vocab_name in self.cache:
            return self.cache[vocab_name]
        
        loader = self.config[vocab_name]['loader']
        path = self.config[vocab_name]['path']
        vocab = loader(path)

        if memoize:
            self.cache[vocab_name] = vocab

        return vocab


# todo - replace the current dict returns of the Loader with this class
class Vocab(collections.UserDict):
    def score_word(self, word, context=None):
        pass
