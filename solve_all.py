"""
Script that looks at the solve paths for all different possible secret words
"""

import atexit
import json
import sys
from typing import Dict, List, Optional

import wordle


# Jankiness so that I get data out even if I interrupt the run XXX
word_to_solve_path : Dict[str, List[str]] = dict()
def dump_progress() -> None:
    with open('solve_path_out.json', 'w') as f:
        json.dump(word_to_solve_path, f)
atexit.register(dump_progress)


def main(args : Optional[List[str]] = None) -> None:
    args = args or sys.argv[1:]

    path = 'words_alpha.txt'
    if len(args) > 0:
        path = args[0]

    with open(path) as f:
        vocab = {w.strip() for w in f.read().split()}
    vocab = {w for w in vocab if len(w) == 5}
    S = wordle.Solver(vocab)

    print(f'Vocab size of {len(vocab)}')

    for i, word in enumerate(vocab):
        W = wordle.Wordle(word)
        solve_path = S.solve(W)
        word_to_solve_path[word] = solve_path

        if i and i % 100 == 0:
            print(i)



if __name__ == '__main__':
    main()

"""
Shoving analysis notes here ^_^

What the distribution of game solves looks like.
It is definitely not the case that all solves happen within 6 guesses

>>> import json
>>> f = open('solve_path_out.json', 'r')
>>> X = json.load(f)
>>> len(X)
15918
>>> import collections
>>> C = collections.Counter()
>>> [C[>>>
>>> for k, vs in X.items():
...     C[len(vs)] += 1
...
>>> C
Counter({4: 5678, 5: 4311, 3: 2313, 6: 1993, 7: 792, 8: 370, 2: 179, 9: 158, 10: 76, 11: 29, 12: 13, 13: 4, 1: 1, 14: 1})
>>> sorted(C.items())
[(1, 1), (2, 179), (3, 2313), (4, 5678), (5, 4311), (6, 1993), (7, 792), (8, 370), (9, 158), (10, 76), (11, 29), (12, 13), (13, 4), (14, 1)]
>>> import pprint
>>> pprint.pprint(sorted(C.items()))
[(1, 1),
 (2, 179),
 (3, 2313),
 (4, 5678),
 (5, 4311),
 (6, 1993),
 (7, 792),
 (8, 370),
 (9, 158),
 (10, 76),
 (11, 29),
 (12, 13),
 (13, 4),
 (14, 1)]
"""
