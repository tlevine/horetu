import re

from sphinx.util.docstrings import prepare_docstring

def description(f):
    try:
        return next(iter(prepare_docstring(f.__doc__)))
    except StopIteration:
        return ''

def docs(f):
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
    if param.default == param.empty:
        return param.name
    else:
        return '--' + param.name

def default(param):
    if param.default != param.empty:
        return param.default
