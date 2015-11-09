from ..main import horetu

def test_flat():
    def f():
        return 8
    assert horetu(f, name = None, description = None, _args = []) == 8
