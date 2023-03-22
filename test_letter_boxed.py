import pytest

from typing import Collection

from letter_boxed import LetterBoxed, get_vocab

__vocab = get_vocab()

@pytest.fixture
def vocab() -> Collection[str]:
    """Load from file once, but copy vocab for each test that wants it"""
    return set(__vocab)

@pytest.fixture
def box_2022_08_21() -> LetterBoxed:
    #return LetterBoxed(['syu', 'cea', 'bpk', 'rni'], 4)
    return LetterBoxed(['syu', 'cea', 'bpk', 'rni'])

@pytest.fixture
def box_2022_08_20() -> LetterBoxed:
    #return LetterBoxed(['mnh', 'oua', 'rqi', 'pvs'], 6)
    return LetterBoxed(['mnh', 'oua', 'rqi', 'pvs'])

def test_valid_subset(box_2022_08_20) -> None:
    assert box_2022_08_20.is_word_valid('improv') 
    assert box_2022_08_20.is_word_valid('vanquish') 

    # This is the key difference...
    assert box_2022_08_20.is_word_valid('quip') 
    assert not box_2022_08_20.is_word_valid('quit') 
    assert not box_2022_08_20.is_word_valid('quir') 
    assert not box_2022_08_20.is_word_valid('quiq') 

    assert not box_2022_08_20.is_word_valid('abba')

#@pytest.mark.xfail(reason="Not implemented yet")
def test_side_constraints_enforced(box_2022_08_20) -> None:
    # o & a on the same side
    assert not box_2022_08_20.is_word_valid('roar')
    # s & p on the same side
    assert not box_2022_08_20.is_word_valid('hasp')

def test_valid_transitions_simple() -> None:
    sides = ['abc', 'def']
    transitions = LetterBoxed._generate_valid_transitions(sides)
    assert transitions == set([
        'ad', 'ae', 'af', 'da', 'ea', 'fa',
        'bd', 'be', 'bf', 'db', 'eb', 'fb',
        'cd', 'ce', 'cf', 'dc', 'ec', 'fc',
    ])

def test_valid_transitions_four_sides() -> None:
    sides = ['abc', 'def', 'ghi', 'jkl']
    transitions = LetterBoxed._generate_valid_transitions(sides)
    assert transitions == set([
        # abc <-> def
        'ad', 'ae', 'af', 'da', 'ea', 'fa',
        'bd', 'be', 'bf', 'db', 'eb', 'fb',
        'cd', 'ce', 'cf', 'dc', 'ec', 'fc',
        # abc <-> ghi
        'ag', 'ah', 'ai', 'ga', 'ha', 'ia',
        'bg', 'bh', 'bi', 'gb', 'hb', 'ib',
        'cg', 'ch', 'ci', 'gc', 'hc', 'ic',
        # abc <-> jkl
        'aj', 'ak', 'al', 'ja', 'ka', 'la',
        'bj', 'bk', 'bl', 'jb', 'kb', 'lb',
        'cj', 'ck', 'cl', 'jc', 'kc', 'lc',
        # def <-> ghi
        'dg', 'dh', 'di', 'gd', 'hd', 'id',
        'eg', 'eh', 'ei', 'ge', 'he', 'ie',
        'fg', 'fh', 'fi', 'gf', 'hf', 'if',
        # def <-> jkl
        'dj', 'dk', 'dl', 'jd', 'kd', 'ld',
        'ej', 'ek', 'el', 'je', 'ke', 'le',
        'fj', 'fk', 'fl', 'jf', 'kf', 'lf',
        # ghi <-> jkl
        'gj', 'gk', 'gl', 'jg', 'kg', 'lg',
        'hj', 'hk', 'hl', 'jh', 'kh', 'lh',
        'ij', 'ik', 'il', 'ji', 'ki', 'li',
    ])

