from collections import OrderedDict

try:
    from inspect import signature as _signature
except ImportError:
    from IPython.utils.signatures import signature as _signature
    from IPython.utils.signatures import Parameter
    PY2 = True
else:
    from inspect import Parameter
    PY2 = False

class AnnotatedParameter(Parameter):
    @classmethod
    def from_parameter(Class, p):
        return Class(p.name, p.kind, default = p.default, annotation = p.annotation)

def _annotated_signature(f):
    s = _signature(f)
    s.parameters = OrderedDict(s.parameters)
    for k in s.parameters:
        s.parameters[k] = AnnotatedParameter.from_parameter(s.parameters[k])
    return s

def signature(f):
    if isinstance(f, annotate):
        s = _annotated_signature(f._function)
        if len(s.parameters) != len(f._types):
            raise ValueError('The annotation must have as many types as the function has arguments.')
        for i, k in enumerate(list(s.parameters)):
            s.parameters[k].annotation = f._types[i]
    else:
        s = _annotated_signature(f)
        if PY2:
            for k in list(s.parameters):
                s.parameters[k].annotation = str

    return s

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
