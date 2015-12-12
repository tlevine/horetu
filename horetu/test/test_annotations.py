from ..annotations import params, annotate

def test_annotations():
    @annotate(str, dict, float, int)
    def f(x, y, a = 3, b = 4):
        pass
    p = params(f)
    assert p[0].annotation == str
    assert p[1].annotation == dict
    assert p[2].annotation == float
    assert p[3].annotation == int

    assert p[0].kind == p[0].POSITIONAL_OR_KEYWORD

def test_annotate():
    @annotate()
    def thingy():
        pass
    assert thingy.__name__ == 'thingy'
    
