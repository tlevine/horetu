import re
from enum import Enum

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
# /usr/local/lib/python3.5/site-packages/sphinx/ext/napoleon/docstring.py
# * WhateverDocString.lines
# * The regexes at the top
# * https://pypi.python.org/pypi/sphinxcontrib-napoleon/
# * http://sphinx-doc.org/latest/extdev/index.html#dev-extensions
# * autodoc-process-docstring event handler
# * docutils-0.12/docutils/core.py
# * fields, field lists
#   * https://www.python.org/dev/peps/pep-0287/#docstring-significant-features
#   * http://www.faqs.org/rfcs/rfc2822.html
# * /usr/local/lib/python3.5/site-packages/sphinx/domains/python.py


def description(f):
    if f.__doc__ is None:
        return ''
    try:
        return next(iter(prepare_docstring(f.__doc__)))
    except StopIteration:
        return ''


def docs(f):
    if f.__doc__ is None:
        raise StopIteration
    for line in prepare_docstring(f.__doc__):
        m = re.match(r'^:param (?:[^:]+ )?([^:]+): (.+)$', line)
        if m:
            yield m.groups()


def nargs(has_keyword_only, param):
    if param.kind == param.VAR_POSITIONAL:
        return '*'
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


def name(param):
    return param.name.replace('_', '-')

def shortflag(param):
    return '-' + param.name[0]

def longflag(param):
    if len(x) > 1:
        return '--' + name(param)

def action(step, param):
    if step == Step.positional:
        return 'store'
    elif step in {Step.keyword1, Step.keyword2}:
        if param.annotation == param.empty:
            return 'store'
        elif param.annotation == bool:
            return 'store_true'
        else:
            return 'store'
    elif step == Step.var_positional:
        return 'append'

class Step(Enum):
    positional = 1
    keyword1 = 2
    var_positional = 3
    keyword2 = 4
