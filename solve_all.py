"""
Script that looks at the solve paths for all different possible secret words
"""

import sys

import wordle

def main(args=None):
    args = args or sys.argv[1:]

    path = 'words_alpha.txt'
    if len(args) > 0:
        path = args[0]

    with open(path) as f:
        vocab = {w.strip() for w in f.read().split()}
    vocab = {w for w in vocab if len(w) == 5}
    S = wordle.Solver(vocab)


if __name__ == '__main__':
    main()
