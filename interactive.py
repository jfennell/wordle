"""
Script to run the Wordle interactive solver.
"""

import sys
from typing import Optional, List

import wordle

def main(args: Optional[List[str]] = None) -> None:
    args = args or sys.argv[1:]

    path = 'words_alpha.txt'
    if len(args) > 0:
        path = args[0]

    with open(path) as f:
        vocab = {w.strip() for w in f.read().split()}
    vocab = {w for w in vocab if len(w) == 5}

    IW = wordle.InteractiveWordle()
    S = wordle.Solver(vocab)

    S.solve(IW)

if __name__ == '__main__':
    main()
