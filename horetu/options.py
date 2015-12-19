import re

from sphinx.util.docstrings import prepare_docstring
from inflection import singularize

# TODO
# * inspect.getdoc
# * inspect.getmodule
# * _build_class__ to register class; set builtins.__build_class__ = f
# * importlib.import_module for docstring
# * garbage collector for types in memory gc.getobjects find types with a name
# * namespace for a function
# * parse the sphinx stuff XXX
# * What about things that don't accept string type?
#   * Nice error message for types that don't accept string in the constructor
# * signature for python 2

class Count(object):
    pass

class Option(object):
    def __init__(self, function = str, default = None):
        self.function = function
        self.default = None
    def __call__(self, x):
        return self.function(x)

class Ignore(object):
    pass

def description(f):
    if f.__doc__ == None:
        return ''
    try:
        return next(iter(prepare_docstring(f.__doc__)))
    except StopIteration:
        return ''

def docs(f):
    if f.__doc__ == None:
        raise StopIteration
    for line in prepare_docstring(f.__doc__):
        m = re.match(r'^:param (?:[^:]+ )([^:]+): (.+)$', line)
        if m:
            yield m.groups()

def nargs(has_keyword_only, param):
    if param.kind == param.VAR_POSITIONAL:
        return '*'
    elif param.annotation == Option:
        return '?'
    elif has_keyword_only and param.kind == param.POSITIONAL_OR_KEYWORD:
        return '?'

def argchoices(param):
    if isinstance(param.annotation, tuple):
        return param.annotation

def argtype(param):
    if param.annotation == param.empty or isinstance(param.annotation, tuple) \
        or (isinstance(param.default, list) and issubclass(param.annotation, list)):
        return str
    else:
        return param.annotation

def name_or_flag(has_keyword_only, param):
    def _name_or_flag(p):
        name = p.name.replace('_', '-')
        if p.default == p.empty or (has_keyword_only and p.kind == p.POSITIONAL_OR_KEYWORD):
            return p.name
        elif len(name) == 1:
            return '-' + name
        else:
            return '--' + name
    try:
        if issubclass(param.annotation, (list, Count)):
            return singularize(_name_or_flag(param))
    except TypeError:
        pass
    return _name_or_flag(param)

def has_keyword_only(params):
    return len(params) and params[-1].kind == params[-1].KEYWORD_ONLY

def dest(param):
    return param.name

def default(param):
    if param.default != param.empty and not isinstance(param.default, bool):
        return param.default

def action(param):
    BOOL_ACTIONS = {True: 'store_false', False: 'store_true'}
    if isinstance(param.default, bool) and param.default in BOOL_ACTIONS:
        return BOOL_ACTIONS[param.default]
    return {
        Count: 'count',
        list: 'append',
    }.get(param.annotation, 'store')
