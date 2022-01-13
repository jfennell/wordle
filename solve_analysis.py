"""
Shoving analysis notes here ^_^

What the distribution of game solves looks like.
It is definitely not the case that all solves happen within 6 guesses

Requires solve_path_out.json to be created
"""

import collections
import json
from typing import Optional, List, Dict

def _display_solve_histogram(hist: Dict[int, int]) -> None:
    total = sum(hist.values())
    print(f"Total words: {sum(hist.values())}")
    print("# guesses: # words that took that many guesses | % of all words | cumulative %")
    cumulation = 0.0
    for solve_length, freq in sorted(hist.items()):
        probability_mass = freq / total
        cumulation += probability_mass
        print(f"{solve_length:02d}: {freq:6d} | {probability_mass:.02f} | {cumulation:.02f}")

def _display_solve(seed: str, guesses: List[str]) -> None:
    path = ' -> '.join(guesses)
    print(f"{seed} ({len(guesses):02d}): {path}")

def _display_heavy_paths(seed_to_guesses: Dict[str, List[str]]) -> None:
    print("The 'hardest to guess' words")
    for seed, guesses in seed_to_guesses.items():
        if len(guesses) <= 10:
            continue

        _display_solve(seed, guesses)

def main(args: Optional[List[str]] = None) -> None:
    with open('solve_path_out.json', 'r') as f:
        X = json.load(f)

    C: Dict[int, int] = collections.Counter()
    for k, vs in X.items():
        C[len(vs)] += 1
    _display_solve_histogram(C)

    print()
    _display_heavy_paths(X)

if __name__ == '__main__':
    main()
