"""
A set of scripts to help out with Letter Boxed
"""

import collections
import sys

from typing import Dict, List, Tuple, Collection, Union, Callable, Optional

from vocab_util import VocabLoader, DERIVED_VOCAB

class LetterBoxed(object):
    #def __init__(self, sides: List[str], word_limit: int) -> None:
    def __init__(self, sides: List[str]) -> None:
        self.sides = sides

        self.allowed_letters = set()
        for side in sides:
            self.allowed_letters.update(side)
        self.valid_transitions = self._generate_valid_transitions(sides)

        #self.word_limit = word_limit

    @staticmethod
    def _generate_valid_transitions(sides):
        valid_transitions = set()

        for i, side_A in enumerate(sides):
            for side_B in sides[i+1:]:
                for c_A in side_A:
                    for c_B in side_B:
                        valid_transitions.add(c_A + c_B)
                        valid_transitions.add(c_B + c_A)

        return valid_transitions

    def is_word_valid(self, word):
        # the word's letters must be a subset of the allowed letters
        if not (set(word) < self.allowed_letters):
            return False

        # the letter adjacencies must be allowed by the set of sides
        for i in range(0, len(word)-1):
            if not word[i:i+2] in self.valid_transitions:
                return False

        return True

    def __repr__(self) -> str:
        #return f'LetterBoxed({self.sides}, {self.word_limit})'
        return f'LetterBoxed({self.sides})'

def filter_vocab(letter_boxed, vocab):
    filtered_vocab = set()
    for i, w in enumerate(vocab):
        if letter_boxed.is_word_valid(w):
            filtered_vocab.add(w)
        if i % 1000 == 0 and i > 0:
            print(f'Filedered {i} of {len(vocab)} words', file=sys.stderr)
    return filtered_vocab
    #return {v for v in vocab if letter_boxed.is_word_valid(v)}

def num_unique_letters(w: str) -> int:
    return len(set(w))

def print_by_num_unique_letters(wordset: set, filter_=None):
    if filter_ is not None:
        filtered_set = [w for w in wordset if filter_(w)]
    L1 = sorted(filtered_set, key=num_unique_letters)
    L2 = sorted(filtered_set)
    L3 = sorted(filtered_set, key=lambda s: s[-1])

    for i in range(len(L1)):
        print(f'{L1[i]:15s}{L2[i]:15s}{L3[i]:15s}')

def main(args: Optional[List[str]] = None) -> None:
    args = args or sys.argv[1:]

    VL = VocabLoader()
    vocab = VL.load(DERIVED_VOCAB)
    letter_box = LetterBoxed(args)
    print(f'Using LetterBox: {letter_box}', file=sys.stderr)
    filtered_vocab = filter_vocab(letter_box, vocab)

    #for w in sorted(filtered_vocab):
    #    print(w)
    
    print(f'Filtered vocabulary size: {len(filtered_vocab)}', file=sys.stderr)
    C = collections.Counter()
    for w in filtered_vocab:
        C[len(w)] += 1
    print(f'Length distribution: {C}', file=sys.stderr)
    ## TODO: Build my own word frequency distribution... maybe form an English wikipedia scrape?

    print('Printing by num unique letters if there are at least 6 distinct letters')
    print_by_num_unique_letters(filtered_vocab, filter_=lambda w: num_unique_letters(w) > 6)

    print('\nShowing the distribution of letters by the number of (filtered) words they appear in')
    letter_distribution = collections.Counter()
    for w in filtered_vocab:
        for c in set(w):
            letter_distribution[c] += 1
    print(f'letter -> # words w/ letter distribution: {letter_distribution.most_common()}')

    print('\nPrinting by num unique letters for the letters of the two lowest frequencies')
    #for (c, n) in letter_distribution.most_common()[-2:]:
    for (c, n) in letter_distribution.most_common()[-1:]:
        print(f'Letter: {c}')
        print_by_num_unique_letters(filtered_vocab, filter_=lambda w: c in w)


if __name__ == '__main__':
    main()
