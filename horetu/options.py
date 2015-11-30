import re

from sphinx.util.docstrings import prepare_docstring

class COUNT(object):
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
        m = re.match(r'^:param ([^:]+ )?([^:]+): (.+)$', line)
        if m:
            k, *v = m.groups()
            yield k, v

def nargs(param):
    if param.kind == param.VAR_POSITIONAL:
        return '*'

def argchoices(param):
    if isinstance(param.annotation, tuple):
        return param.annotation

def argtype(param):
    if param.annotation == param.empty or isinstance(param.annotation, tuple):
        return str
    else:
        return param.annotation

def name_or_flags(param):
    name = param.name.replace('_', '-')
    if param.default == param.empty:
        return name
    elif len(name) == 1:
        return '-' + name
    else:
        return '--' + name

def default(param):
    if param.default != param.empty:
        return param.default

def action(param):
    return {
        COUNT: 'count',
        list: 'append',
    }.get(param.annotation, 'store')
