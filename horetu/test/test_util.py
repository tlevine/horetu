from ..util import expand_dict_keys

def test_expand_dict_keys():
    x = {'a': {'b': ['aoeu',',u'], 'c': {'d': 89}}, 'e': lambda:8}
    y = {'a b', 'a c d', 'e'}
    assert set(expand_dict_keys(x)) == y
