import re
from functools import partial
import operator
from inspect import signature, Parameter
from configparser import ConfigParser
from collections import Counter

from . import options

FLAG = re.compile(r'^-?(-[^-]).*')
Step = options.Step

def _filename(x):
    if not os.path.isfile(x):
        raise ValueError('"%s" is not a file.' % x)
    return x


def one(configuration_file, configuration_section,
        parser, f):
    sig = signature(f)
    helps = dict(options.docs(f))

    if configuration_file:
        c = ConfigParser()
        c.read(configuration_file)
        if configuration_section in c.sections():
            defaults = dict(c[configuration_section])
        else:
            defaults = {}
    else:
        defaults = {}

    kind = None
    steps = []
    sfs = single_character_flags(sig)
    k2 = has_step(Step.keyword2, sig)
    for i, param in enumerate(sig.parameters.values()):
        st = step(kind, param)
        steps.append(st)

        args = options.choose_name_args(sfs, k2, st, param)
        argtype = options.argtype(param)
        config_file_arg_name = param.name

        kwargs = dict(nargs=options.nargs(k2, st),
                      action=options.action(st, param),
                      type=argtype,
                      choices=options.argchoices(param),
                      help=helps.get(param.name, ''))

        if config_file_arg_name in defaults:
            kwargs['default'] = argtype(defaults[config_file_arg_name])
        elif param.default != param.empty:
            kwargs['default'] = param.default

        if args[0].startswith('-'):
            kwargs['dest'] = param.name

        if kwargs['action'] in {'store_true', 'store_false', 'count'}:
            del(kwargs['choices'])
            del(kwargs['type'])
            del(kwargs['nargs'])
        parser.add_argument(*args, **kwargs)

    def g(parsed_args):
        args = []
        kwargs = {}

        kind = None
        for i, param in enumerate(sig.parameters.values()):
            st = step(kind, param)
            arg = getattr(parsed_args, param.name)
            if st == Step.positional:
                args.append(arg)
            elif st == Step.var_positional:
                args.extend(arg)
            else:
                kwargs[param.name] = arg
        return f(*args, **kwargs)
    return g

KINDS = {
    Step.positional: {
        Parameter.POSITIONAL_ONLY,
        Parameter.POSITIONAL_OR_KEYWORD
    },
    Step.keyword1: {Parameter.POSITIONAL_OR_KEYWORD},
    Step.var_positional: {Parameter.VAR_POSITIONAL},
    Step.keyword2: {Parameter.KEYWORD_ONLY},
}

def has_step(the_step, sig):
    kind = None
    for i, param in enumerate(sig.parameters.values()):
        st = step(kind, param)
        if st == the_step:
            return True
    return False

def single_character_flags(sig):
    kind = None
    x = ['-h']
    k2 = has_step(Step.keyword2, sig)
    for i, param in enumerate(sig.parameters.values()):
        st = step(kind, param)
        if k2:
            if st == Step.keyword2:
                x.append('-' + param.name[0])
        else:
            if st == Step.keyword1:
                x.append('-' + param.name[0])
    return set(name for name,count in Counter(x).items() if count > 1)

def step(prev_kind, param):
    if param.kind in KINDS[Step.positional].union(KINDS[Step.keyword1]):
        if param.default == param.empty:
            this_kind = Step.positional
        else:
            this_kind = Step.keyword1
    elif param.kind in KINDS[Step.var_positional]:
        this_kind = Step.var_positional
    elif param.kind in KINDS[Step.keyword2]:
        this_kind = Step.keyword2
    else:
        raise ValueError(
            'Variable keyword args (**kwargs) are not allowed. You may implement your own key-value parser that takes the result of variable positional args (*args).')

    if prev_kind and this_kind < prev_kind:
        raise ValueError('This should not happen.')

    return this_kind
