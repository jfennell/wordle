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


class InteractiveWordle(object):
    """
    Interactive solver to help a human 
    efficiently solve a Wordle puzzle
    """
    def __init__(self):
        self.num_guesses = 0

    def ask(self, guesses):
        while True:
            print(f'The solver\'s top guesses are:')
            for guess in guesses:
                print(f' * {guess}')
            print('\nWhat guess did you pick?')
            ask = input(' > ').lower()
            if not len(ask) == 5:
                print('Invalid input, Try again.\n')
                continue

            print('What is the feedback?')
            print('Enter a 5 letter answer where')
            print(' N => no match. That letter is not in the secret word')
            print(' P => partial match. That letter is in the world, but not at that position')
            print(' E => exact match. That letter is in the world at that position')
            raw_answer = input(' > ').lower()

            if not (set(raw_answer).issubset(set('npe')) and len(raw_answer) == 5):
                print('Invalid input. Try again.\n')
                continue

            answer = []
            for c in raw_answer:
                if c == 'n':
                    answer.append(Match.NO)
                elif c == 'p':
                    answer.append(Match.IN_WORD)
                elif c == 'e':
                    answer.append(Match.AT_POSITION)
                else:
                    raise ValueError(f'"{raw_answer}" is not a valid input')

            return ask, answer

    def is_win(self, answer):
        return answer == [Match.AT_POSITION]*5

    def __repr__(self):
        return 'InteractiveWordle()'


class Solver(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def solve(self, wordle_instance, ask_multi=False):
        words = list(self.vocab)

        while True:
            words = self._predict_best_wordle_guesses(words)

            if not words:
                raise ValueError(f'Failed to solve {wordle_instance}')

            ask = words[0]
            if not ask_multi:
                answer = wordle_instance.ask(ask)
            else:
                ask, answer = wordle_instance.ask(words[:10])

            if wordle_instance.is_win(answer):
                print(f"Winner! {ask}")
                break

            _filter = self._build_filter(ask, answer)
            words = [w for w in words if _filter(w)]

        return ask

    @classmethod
    def _score_word(cls, word, letter_counts):
        letters = set(word)
        return sum(letter_counts.get(l, 0) for l in letters)

    @classmethod
    def _predict_best_wordle_guesses(cls, words):
        """
        Given a set of wordle words, analyze which word will
        heuristically best explore the remaining vocabulary.
        """
        letter_counts = collections.Counter(''.join(words))

        best_guesses = sorted(
            words, 
            key=lambda w: cls._score_word(w, letter_counts),
            reverse=True
        )

        return best_guesses

    @classmethod
    def _build_filter(cls, ask, answer):
        """Given a word we "asked" and a list(Match), referred to an an Answer,
        construct a filter that only matches words that conform to the constraints
        from the answer
        """

        filter_list = []
        for i, (c, m) in enumerate(zip(ask, answer)):
            if m == Match.NO:
                filter_list.append(cls._build_no_match(c))
            elif m == Match.IN_WORD:
                filter_list.append(cls._build_in_word_match(c, i))
            elif m == Match.AT_POSITION:
                filter_list.append(cls._build_at_position_match(c, i))

        def word_filter(word):
            return all(f(word) for f in filter_list)

        return word_filter

    @classmethod
    def _build_no_match(cls, c):
        """Build a filter function that passes when word does *not* contain `c`"""
        def no_match(word):
            return c not in word
        return no_match

    @classmethod
    def _build_in_word_match(cls, c, i):
        """Build a filter function that passes when word contains `c`, but not at w[i]"""
        def in_word_match(word):
            return (c in word) and (word[i] != c)
        return in_word_match

    @classmethod
    def _build_at_position_match(cls, c, i):
        """Build a filter function that passes when word has `c` at position `i`"""
        def at_position_match(word):
            return word[i] == c
        return at_position_match

