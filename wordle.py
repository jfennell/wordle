"""
A simulator to run the Wordle game

Wordle object encapsulates the gamestate.

Instantiate the Wordle object with a word

Ask the World object with guess words
- TODO: Enforce "in-vocab", length & chracter constraints
- Return: Answer. An object representing what matched & didn't
"""

import collections
import enum

class Match(enum.Enum):
    NO = enum.auto()
    IN_WORD = enum.auto()
    AT_POSITION = enum.auto()

class Wordle(object):
    def __init__(self, secret_word):
        self.secret_word = secret_word
        self.secret_word_letters = set(secret_word)
        self.num_guesses = 0

    def ask(self, guess):
        self.num_guesses += 1

        answer = []
        for i, c in enumerate(guess):
            if c == self.secret_word[i]:
                answer.append(Match.AT_POSITION)
            elif c in self.secret_word_letters:
                answer.append(Match.IN_WORD)
            else:
                answer.append(Match.NO)
        return answer

    def is_win(self, answer):
        return answer == [Match.AT_POSITION]*len(self.secret_word)

    def __repr__(self):
        return f'Wordle({self.secret_word}, {self.num_guesses})'


class Solver(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def solve(self, wordle_instance):
        words = list(self.vocab)

        while True:
            words = self._predict_best_wordle_guesses(words)

            if not words:
                raise ValueError(f'Failed to solve {wordle_instance}')

            ask = words[0]
            answer = wordle_instance.ask(ask)

            if wordle_instance.is_win(answer):
                print(f"Winner! {ask}")
                break

            _filter = self._build_filter(ask, answer)
            words = [w for w in words if _filter(w)]

        return ask

    def _score_word(self, word, letter_counts):
        letters = set(word)
        return sum(letter_counts.get(l, 0) for l in letters)

    def _predict_best_wordle_guesses(self, words):
        """
        Given a set of wordle words, analyze which word will
        heuristically best explore the remaining vocabulary.
        """
        letter_counts = collections.Counter(''.join(words))

        best_guesses = sorted(
            words, 
            key=lambda w: self._score_word(w, letter_counts),
            reverse=True
        )

        return best_guesses

    def _build_filter(self, ask, answer):
        """Given a word we "asked" and a list(Match), referred to an an Answer,
        construct a filter that only matches words that conform to the constraints
        from the answer
        """

        #import pdb; pdb.set_trace()
        filter_list = []
        for i, (c, m) in enumerate(zip(ask, answer)):
            if m == Match.NO:
                filter_list.append(lambda word: c not in word)
            elif m == Match.IN_WORD:
                filter_list.append(lambda word: (c in word) and (word[i] != c))
            elif m == Match.AT_POSITION:
                filter_list.append(lambda word: word[i] == c)

        def word_filter(word):
            return all(f(word) for f in filter_list)

        return word_filter

