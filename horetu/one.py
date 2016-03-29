import re
from functools import partial
import operator
from inspect import signature, Parameter
from configparser import ConfigParser
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

    single_character_flags = {'-h'}
    kind = None
    steps = []
    for i, param in enumerate(sig.parameters.values()):
        st = step(kind, param)
        steps.append(st)

        args = options.choose_name_args(single_character_flags, st, param)
        argtype = options.argtype(param)
        config_file_arg_name = options.name(param)

        if config_file_arg_name in defaults:
            default = argtype(defaults[config_file_arg_name])
        elif param.default == param.empty:
            default = None
        else:
            default = param.default

        kwargs = dict(nargs=options.nargs(st, param),
                      action=options.action(st, param),
                     #dest=param.name,
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
        kwargs = {name:getattr(parsed_args, name) for name in sig.parameters}
        return f(**kwargs)
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
