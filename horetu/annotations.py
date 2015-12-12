from copy import copy
from functools import wraps

try:
    from inspect import signature
except ImportError:
    from IPython.utils.signatures import signature
    from IPython.utils.signatures import Parameter
    PY2 = True
else:
    from inspect import Parameter
    PY2 = False

class AnnotatedParameter(Parameter):
    @classmethod
    def from_parameter(Class, p, annotation = None):
        if not annotation:
            annotation = p.annotation
        return Class(p.name, p.kind, default=p.default, annotation=annotation)

def params(f):
    ps = list(signature(f).parameters.values())
    if hasattr(f, '_types'):
        if len(ps) != len(f._types):
            raise ValueError('The annotation must have as many types as the function has arguments.')
        for i in range(len(ps)):
            ps[i] = AnnotatedParameter.from_parameter(ps[i], annotation=f._types[i])
    else:
        if PY2:
            for i in range(len(ps)):
                ps[i] = AnnotatedParameter.from_parameter(ps[i], annotation=str)

    return ps

def annotate(*types):
    '''
    Annotate a Python 2 function. ::

        @annotate(int, int)
        def f(x, y = 8):
            return x + y
    '''
    def decorator(f):
        @wraps(f)
        def g(*args, **kwargs):
            return f(*args, **kwargs)
        g._types = types
        return g
    return decorator
