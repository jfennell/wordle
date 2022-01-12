import pytest

from wordle import Match, Wordle, Solver

def __load_vocab():
    path = 'words_alpha.txt'
    _filter = lambda w: len(w) == 5

    with open(path) as f:
        words = {w.strip() for w in f.read().split()}

    if _filter is not None:
        words = {w for w in words if _filter(w)}

    return words
__vocab = __load_vocab()

@pytest.fixture
def vocab():
    """Load from file once, but copy vocab for each test that wants it"""
    return set(__vocab)


def test_enum_words():
    assert Match.NO == Match.NO
    assert Match.NO != Match.AT_POSITION

def test_exact_guess():
    W = Wordle("hello")
    result = W.ask("hello")
    assert result == [Match.AT_POSITION]*5
    assert W.num_guesses == 1
    assert W.is_win(result)

def test_missed_guess():
    W = Wordle("hello")
    result = W.ask("marks")
    assert result == [Match.NO]*5
    assert W.num_guesses == 1
    assert not W.is_win(result)

def test_mixed_guess():
    W = Wordle("crows")
    result = W.ask("works")
    assert result == [Match.IN_WORD, Match.IN_WORD, Match.IN_WORD, Match.NO, Match.AT_POSITION]
    assert W.num_guesses == 1
    assert not W.is_win(result)

def test_longer_word():
    W = Wordle("transcribe")
    result = W.ask("prescribes")
    assert result == [
        Match.NO, Match.AT_POSITION, 
        Match.IN_WORD, Match.IN_WORD,
        Match.IN_WORD, Match.IN_WORD,
        Match.IN_WORD, Match.IN_WORD,
        Match.IN_WORD, Match.IN_WORD,
    ]
    assert W.num_guesses == 1
    assert not W.is_win(result)


def test_solve(vocab):
    W = Wordle("hello")
    S = Solver(vocab)
    solution = S.solve(W)
    assert solution[-1] == "hello"
    assert W.num_guesses < 10 


def test_build_filter_simple_at_position():
    S = Solver([])
    ask = "a"
    answer = [Match.AT_POSITION]
    _filter = S._build_filter(ask, answer)
    assert _filter("a")
    assert not _filter("b")
    assert _filter("aardvark")

def test_build_filter_no_match():
    S = Solver([])
    ask = "a"
    answer = [Match.NO]
    _filter = S._build_filter(ask, answer)
    assert not _filter("a")
    assert _filter("b")
    assert not _filter("aardvark")
    assert not _filter("bark")

def test_build_filter_no_match_longer():
    S = Solver([])
    ask = "abc"
    answer = [Match.NO]*3
    _filter = S._build_filter(ask, answer)
    assert not _filter("c")
    assert not _filter("b")
    assert not _filter("a")
    assert not _filter("cab")
    assert _filter("def")
    assert not _filter("defb")

def test_build_filter_simple_in_word():
    S = Solver([])
    ask = "a"
    answer = [Match.IN_WORD]
    _filter = S._build_filter(ask, answer)
    assert not _filter("a")
    assert not _filter("b")
    assert not _filter("aardvark")
    assert _filter("bark")

def test_build_filter_complex():
    S = Solver([])
    ask = "help"
    answer = [Match.NO, Match.AT_POSITION, Match.IN_WORD, Match.IN_WORD]
    _filter = S._build_filter(ask, answer)
    #import pdb; pdb.set_trace()
    assert _filter("pexl")
    assert not _filter("h")
    assert _filter("xeeelp")
    assert not _filter("xelp")
    assert _filter("perl")
