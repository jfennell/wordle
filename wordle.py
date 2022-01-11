import collections
import sys
import os.path

def get_words(path, _filter=None):
    with open(path) as f:
        words = {w.strip() for w in f.read().split()}

    if _filter is not None:
        words = {w for w in words if _filter(w)}

    return words

def score_word(word, letter_counts):
    letters = set(word)
    return sum(letter_counts.get(l, 0) for l in letters)

def main(args=None):
    args = args or sys.argv[1:]

    path = args[0]
    words = get_words(path, _filter=lambda w: len(w) == 5)

    print(f"Filtered down to {len(words)} words")

    letter_counts = collections.Counter(''.join(words))
    print("\nThe most common letters are:")
    for (k, v) in letter_counts.most_common():
        print(f"{k}: {v}")

    words = sorted(words, key=lambda w: score_word(w, letter_counts), reverse=True)
    print()
    print("\nThe best starting words")
    for w in words[:10]:
        print(w)

    print("\n*** Chose `arose` ***")
    # arose
    # r & o are in, a & s are out, e is at the end
    def result_filter(w):
        if 'a' in w or 's' in w:
            return False
        if w[1] == 'r' or w[2] == 'o':
            return False
        if not ('r' in w and 'o' in w):
            return False
        if w[4] != 'e':
            return False
        return True

    words = {w for w in words if result_filter(w)}
    print(f"\nFiltered down to {len(words)} words")
    print("A few samples:")
    poppable_copy = set(words)
    for _ in range(10):
        print(poppable_copy.pop())

    letter_counts = collections.Counter(''.join(words))
    print("\nThe most common letters are:")
    for (k, v) in letter_counts.most_common():
        print(f"{k}: {v}")

    words = sorted(words, key=lambda w: score_word(w, letter_counts), reverse=True)
    print()
    print("\nThe best 2nd round words")
    for w in words[:10]:
        print(w)

    print("\n*** Chose `route` ***")
    # route
    # 'r' is not at the start. 'o' & 'e' are right. 'u', 't' out
    def result_filter(w):
        if 'u' in w or 't' in w:
            return False
        if w[0] == 'r':
            return False
        if not ('r' in w):
            return False
        if w[1] != 'o' or w[4] != 'e':
            return False
        return True

    words = {w for w in words if result_filter(w)}
    print(f"\nFiltered down to {len(words)} words")
    print("A few samples:")
    poppable_copy = set(words)
    for _ in range(10):
        print(poppable_copy.pop())

    letter_counts = collections.Counter(''.join(words))
    print("\nThe most common letters are:")
    for (k, v) in letter_counts.most_common():
        print(f"{k}: {v}")

    words = sorted(words, key=lambda w: score_word(w, letter_counts), reverse=True)
    print()
    print("\nThe best 2nd round words")
    for w in words[:10]:
        print(w)

    print("\n*** Chose `forge` ***")
    # forge
    # 'orge' is all correct and in the right places. 'f' is not in
    def result_filter(w):
        if 'f' in w:
            return False
        if w[1] != 'o' or w[2] != 'r' or w[3] != 'g' or  w[4] != 'e':
            return False
        return True

    words = {w for w in words if result_filter(w)}
    print(f"\nFiltered down to {len(words)} words")
    print("A few samples:")
    poppable_copy = set(words)
    for _ in range(10):
        print(poppable_copy.pop())

    letter_counts = collections.Counter(''.join(words))
    print("\nThe most common letters are:")
    for (k, v) in letter_counts.most_common():
        print(f"{k}: {v}")

    words = sorted(words, key=lambda w: score_word(w, letter_counts), reverse=True)
    print()
    print("\nThe best 3nd round words")
    for w in words[:10]:
        print(w)




if __name__ == '__main__':
    main()
