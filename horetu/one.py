import re
from functools import partial
import operator
from inspect import signature, Parameter
from configparser import ConfigParser
from enum import Enum
from . import options

FLAG = re.compile(r'^-?(-[^-]).*')


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

    single_character_flags = {'-h'}
    kind = None
    for i, param in enumerate(sig.parameters.values()):
        st = step(kind, param)

        args = choose_name_args(single_character_flags, st, param)
        argtype = options.argtype(param)
        config_file_arg_name = options.name(param)

        if config_file_arg_name in defaults:
            default = argtype(defaults[config_file_arg_name])
        elif param.default == param.empty:
            default = None
        else:
            default = param.default

        print(st)
        if st == Step.positional:
            action = 'store'
        elif st in {Step.keyword1, Step.keyword2}:
            if param.annotation == param.empty:
                action = 'store'
            elif param.annotation == bool:
                action = 'store_true'
            else:
                action = 'store'
        elif st == Step.var_positional:
            action = 'append'
        kwargs = dict(nargs=options.nargs(st, param),
                      action=action,
                      dest=options.dest(param),
                      type=argtype,
                      choices=options.argchoices(param),
                      help=helps.get(param.name, ''),
                      default=default)
        if kwargs['action'] in {'store_true', 'store_false', 'count'}:
            del(kwargs['choices'])
            del(kwargs['type'])
            del(kwargs['nargs'])
        parser.add_argument(*args, **kwargs)

    def g(parsed_args):
        args = [getattr(parsed_args, attr)
                for attr in _get_args(False, has_keyword_only, params)]
        for param in params:
            if param.kind == param.VAR_POSITIONAL:
                args.extend(getattr(parsed_args, param.name))
        kwargs = {attr: getattr(parsed_args, attr)
                  for attr in _get_args(True, has_keyword_only, params)}
        return f(*args, **kwargs)
    return g

def choose_name_args(single_character_flags, st, param):
    if st == Step.positional:
        args = options.name(param),
    elif st in {Step.keyword1, Step.keyword2}:
        lf = options.longflag(param)
        sf = options.shortflag(param)
        if sf in single_character_flags:
            args = lf,
        else:
            single_character_flags.add(sf)
            if lf:
                args = sf, lf
            else:
                args = sf,
    elif st == Step.var_positional:
        args = options.name(param),
    else:
        raise ValueError('Bad step: %s' % st)

class Step(Enum):
    positional = 1
    keyword1 = 2
    var_positional = 3
    keyword2 = 4

KINDS = {
    Step.positional: {
        Parameter.POSITIONAL_ONLY,
        Parameter.POSITIONAL_OR_KEYWORD
    },
    Step.keyword1: {Parameter.POSITIONAL_OR_KEYWORD},
    Step.var_positional: {Parameter.VAR_POSITIONAL},
    Step.keyword2: {Parameter.KEYWORD_ONLY},
}

def step(prev_kind, param):
    if param.kind in KINDS[Step.positional].union(KINDS[Step.keyword1]):
        if param.default == param.empty:
            this_kind = Step.positional
        else:
            this_kind = Step.keyword1
    elif param.kind in KINDS[Step.var_positional]:
        this_kind = Step.var_positional
    elif param.kind in KINDS[Step.keyword_only]:
        this_kind = Step.keyword_only
    else:
        raise ValueError(
            'Variable keyword args (**kwargs) are not allowed. You may implement your own key-value parser that takes the result of variable positional args (*args).')

    if prev_kind and this_kind < prev_kind:
        raise ValueError('This should not happen.')

    return this_kind
