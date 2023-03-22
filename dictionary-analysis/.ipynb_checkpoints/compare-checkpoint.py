import csv
import sys

# Arguable that this could be memoized, paramatrized by path
def get_words_alpha(path='words_alpha.txt'):
    with open(path) as f:
        vocab = {w.strip():1 for w in f.read().split()}
    return vocab

def get_unigram_freq(path='unigram_freq.csv'):
    with open(path) as f:
        vocab = {}
        for l in f.read().split():
            w, c = l.split(',', 2)
            vocab[w] = c
    return vocab

def main():
    unigram_freq = get_unigram_freq()
    words_alpha = get_words_alpha()

    unigram_freq_s = set(unigram_freq)
    words_alpha_s = set(words_alpha)

    only_unigram_freq = unigram_freq_s.difference(words_alpha_s)
    only_words_alpha = words_alpha_s.difference(unigram_freq_s)
    common_words = unigram_freq_s.intersect(words_alpha_s)

    
     
if __name__ == '__main__':
    main()
