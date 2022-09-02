"""
Script to run the Wordle interactive solver.
"""

import sys
from typing import Optional, List

import wordle
from vocab_util import VocabLoader, WORDS_ALPHA_VOCAB, DERIVED_VOCAB

def main(args: Optional[List[str]] = None) -> None:
    args = args or sys.argv[1:]

    VL = VocabLoader()
    if len(args) == 0:
        vocab = VL.load(WORDS_ALPHA_VOCAB)
    else:
        # Rare case
        vocab = VL.load(args[0])

    vocab = {w for w in vocab if len(w) == 5}

    IW = wordle.InteractiveWordle()
    S = wordle.Solver(vocab)

    S.solve(IW)

if __name__ == '__main__':
    main()
