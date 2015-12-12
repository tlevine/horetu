from ..annotations import signature, annotate

def test_annotations():
    @annotate(str, dict, float, int)
    def f(x, y, a = 3, b = 4):
        pass
    p = signature(f).parameters
    assert p['x'].annotation == str
    assert p['y'].annotation == dict
    assert p['a'].annotation == float
    assert p['b'].annotation == int

    assert p['x'].kind == p['x'].POSITIONAL_OR_KEYWORD
