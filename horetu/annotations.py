from collections import OrderedDict

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
    if isinstance(f, annotate):
        ps = list(signature(f._function).parameters.values())
        if len(ps) != len(f._types):
            raise ValueError('The annotation must have as many types as the function has arguments.')
        for i in range(len(ps)):
            ps[i] = AnnotatedParameter.from_parameter(ps[i], annotation=f._types[i])
    else:
        ps = list(signature(f).parameters.values())
        if PY2:
            for i in range(len(ps)):
                ps[i] = AnnotatedParameter.from_parameter(ps[i], annotation=str)

    return ps

class annotate(object):
    '''
    Annotate a Python 2 function. ::

        @annotate(int, int)
        def f(x, y = 8):
            return x + y
    '''
    def __init__(self, *types):
        self._types = types
    def __call__(self, function):
        self._function = function
        return self
