import pytest

import vocab_util
from vocab_util import VocabLoader


def test_load_vocab_memoize():
    config = dict(vocab_util._loader_config) 
    TEST_VOCAB = 'test_vocab'

    call_count = [0]
    def test_loader(_):
        call_count[0] += 1
        return dict(foo=3, bar=2, baz=1)
    
    config[TEST_VOCAB] = dict(
        path=TEST_VOCAB,
        loader=test_loader
    )

    VL = VocabLoader(config=config)
    vocab = VL.load(TEST_VOCAB)
    assert vocab.get('foo') == 3
    assert vocab.get('bar') == 2
    assert vocab.get('baz') == 1
    assert len(vocab) == 3
    assert call_count[0] == 1

    vocab_2 = VL.load(TEST_VOCAB)
    assert vocab == vocab_2
    assert call_count[0] == 1

    VL.load(TEST_VOCAB, memoize=False)
    assert vocab == vocab_2
    assert call_count[0] == 2

def test_load_vocab():
    config = dict(vocab_util._loader_config) 
    TEST_VOCAB = 'test_vocab'

    config[TEST_VOCAB] = dict(
        path=TEST_VOCAB,
        loader=lambda _: dict(foo=5),
    )

    VL = VocabLoader(config=config)
    vocab = VL.load(TEST_VOCAB)
    assert vocab.get('foo') == 5
    assert len(vocab) == 1

@pytest.mark.smoketest
def test_smoketest():
    VL = VocabLoader()
    VL.load(vocab_util.WORDS_ALPHA_VOCAB)
    VL.load(vocab_util.UNIGRAM_FREQ_VOCAB)
    VL.load(vocab_util.DERIVED_VOCAB)
    assert True
