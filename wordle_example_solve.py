import collections
import sys
import os.path
from typing import Callable, Optional, Collection, Dict, List

StrFilter = Callable[[str], bool]

DEBUG = True

def get_words(path: str, _filter: Optional[StrFilter] = None) -> Collection[str]:
    with open(path) as f:
        words = {w.strip() for w in f.read().split()}

    if _filter is not None:
        words = {w for w in words if _filter(w)}

    return words

def score_word(word: str, letter_counts: Dict[str, int]) -> int:
    letters = set(word)
    return sum(letter_counts.get(l, 0) for l in letters)

def predict_best_wordle_guesses(words: Collection[str]) -> List[str]:
    """
    Given a set of wordle words, analyze which word will
    heuristically best explore the remaining vocabulary.
    """
    letter_counts = collections.Counter(''.join(words))

    # TODO: Clean this up. Either remove or add actual log statements
    if DEBUG:
        print("\nThe most common letters are:")
        for (k, v) in letter_counts.most_common():
            print(f"{k}: {v}")

    best_guesses = sorted(
        words, 
        key=lambda w: score_word(w, letter_counts),
        reverse=True
    )

    if DEBUG:
        print()
        print("\nThe best starting words")
        for w in best_guesses[:10]:
            print(w)

    return best_guesses

def filter_words(words: Collection[str], result_filter: StrFilter) -> Collection[str]:
    words = {w for w in words if result_filter(w)}

    if DEBUG:
        print(f"\nFiltered down to {len(words)} words")
        print("A few samples:")
        poppable_copy = set(words)
        for _ in range(10):
            print(poppable_copy.pop())

    return words

def main(args: Optional[List[str]] = None) -> None:
    args = args or sys.argv[1:]

    path = args[0]
    words = get_words(path, _filter=lambda w: len(w) == 5)

    print(f"Filtered down to {len(words)} words")

    words = predict_best_wordle_guesses(words)

    print("\n*** Chose `arose` ***")
    # arose
    # r & o are in, a & s are out, e is at the end
    def result_filter_1(w: str) -> bool:
        if 'a' in w or 's' in w:
            return False
        if w[1] == 'r' or w[2] == 'o':
            return False
        if not ('r' in w and 'o' in w):
            return False
        if w[4] != 'e':
            return False
        return True

    words = filter_words(words, result_filter_1)
    words = predict_best_wordle_guesses(words)

    print("\n*** Chose `route` ***")
    # route
    # 'r' is not at the start. 'o' & 'e' are right. 'u', 't' out
    def result_filter_2(w: str) -> bool:
        if 'u' in w or 't' in w:
            return False
        if w[0] == 'r':
            return False
        if not ('r' in w):
            return False
        if w[1] != 'o' or w[4] != 'e':
            return False
        return True

    words = filter_words(words, result_filter_2)
    words = predict_best_wordle_guesses(words)

    print("\n*** Chose `forge` ***")
    # forge
    # 'orge' is all correct and in the right places. 'f' is not in
    def result_filter_3(w: str) -> bool:
        if 'f' in w:
            return False
        if w[1] != 'o' or w[2] != 'r' or w[3] != 'g' or  w[4] != 'e':
            return False
        return True

    words = filter_words(words, result_filter_3)
    words = predict_best_wordle_guesses(words)



if __name__ == '__main__':
    main()
