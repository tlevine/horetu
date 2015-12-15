import re

from sphinx.util.docstrings import prepare_docstring
from inflection import singularize

class COUNT(object):
    pass

class OPTIONAL(object):
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

def nargs(param):
    if param.kind == param.VAR_POSITIONAL:
        return '*'
    elif param.annotation == OPTIONAL:
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

def _name_or_flag(param, keyword):
    name = param.name.replace('_', '-')
    if param.default == param.empty or (keyword and param.kind == param.POSITIONAL_OR_KEYWORD):
        return param.name
    elif len(name) == 1:
        return '-' + name
    else:
        return '--' + name

def has_keyword_only(params):
    try:
        p = next(reversed(params))
    except StopIteration:
        return False
    else:
        return p.kind == p.KEYWORD_ONLY

def name_or_flags(params):
    k = has_keyword_only(params)
    for param in params:
        try:
            if issubclass(param.annotation, (list, COUNT)):
                yield singularize(_name_or_flag(param, k))
                continue
        except TypeError:
            pass
        yield _name_or_flag(param, k)

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
        COUNT: 'count',
        list: 'append',
    }.get(param.annotation, 'store')
