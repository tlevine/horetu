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


def nargs(has_k2, step):
    if has_k2 and step == Step.keyword1:
        return '?'
    elif step == Step.var_positional:
        return '*'

def argchoices(param):
    if isinstance(param.annotation, tuple):
        return param.annotation

def argtype(param):
    if param.annotation == param.empty or \
        isinstance(param.annotation, tuple) or \
        param.kind == param.VAR_POSITIONAL or \
        (isinstance(param.default, list) and \
            issubclass(param.annotation, list)):
        return str
    else:
        return param.annotation


def shortflag(param):
    return '-' + param.name[0]

def longflag(param):
    if len(param.name) > 1:
        x = param.name.replace('_', '-')
        if param.annotation == list:
            y = singularize(x)
        else:
            y = x
        return '--' + y

def dest(param):
    if param.annotation == list and param.default != param.empty:
        return singularize(param.name)

def action(step, param):
    if step == Step.positional:
        return 'store'
    elif step in {Step.keyword1, Step.keyword2}:
        if param.annotation == param.empty:
            if param.default == True:
                return 'store_false'
            elif param.default == False:
                return 'store_true'
            else:
                return 'store'
        elif param.annotation == bool:
            if param.default == param.empty or param:
                return 'store_false'
            else:
                return 'store_true'
        elif param.annotation == list:
            return 'append'
        else:
            return 'store'
    elif step == Step.var_positional:
        return 'store'

class Step(Enum):
    positional = 1
    keyword1 = 2
    var_positional = 3
    keyword2 = 4

def choose_name_args(single_character_flags, has_k2, st, param):
    if st == Step.positional or (has_k2 and st == Step.keyword1):
        args = param.name,
    elif st in {Step.keyword1, Step.keyword2}:
        lf = longflag(param)
        sf = shortflag(param)
        if lf and sf in single_character_flags:
            args = lf,
        else:
            if lf:
                args = sf, lf
            else:
                args = sf,
    elif st == Step.var_positional:
        args = param.name,
    else:
        raise ValueError('Bad step: %s' % st)
    return args

