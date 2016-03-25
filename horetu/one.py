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
    s = signature(f)
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
    for i, param in enumerate(params.values()):
        if param.kind == param.VAR_KEYWORD:
            raise ValueError(
                'Variable keyword args (**kwargs) are not allowed. You may implement your own key-value parser that takes the result of variable positional args (*args).')

        if param.kind not in allowed_kinds[step]:
            step += 1
            if step >= len(allowed_kinds):
                raise ValueError('This should never happen.')
            continue


        name_or_flag = get_name_or_flag(param)
        m = re.match(FLAG, name_or_flag)
        if m and step >= 2 and m.group(1) in single_character_flags:
            args = name_or_flag,
        else:
            args = (name_or_flag, m.group(1))
            single_character_flags.add(m.group(1))

        argtype = options.argtype(param)
        config_file_arg_name = name_or_flag.lstrip('-')
        if config_file_arg_name in defaults:
            default = argtype(defaults[config_file_arg_name])
        else:
            default = options.default(param)
        kwargs = dict(nargs=options.nargs(has_keyword_only, param),
                      action=options.action(param),
                      dest=options.dest(param),
                      type=argtype,
                      choices=options.argchoices(param),
                      help=helps.get(param.name, ''),
                      default=default)
        if kwargs['action'] in {'store_true', 'store_false', 'count'}:
            del(kwargs['choices'])
            del(kwargs['type'])
            del(kwargs['nargs'])
        if not name_or_flag.startswith('-'):
            del(kwargs['dest'])
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

class Kind(Enum):
    positional_or_keyword = 1
    var_positional = 2
    keyword_only = 3

KINDS = {
    positional_or_keyword: {
        Parameter.POSITIONAL_ONLY,
        Parameter.POSITIONAL_OR_KEYWORD
    },
    var_positional: {Parameter.VAR_POSITIONAL},
    keyword_only: {Parameter.KEYWORD_ONLY},
}

def step(prev_kind, param):
    if param.kind in kinds['positional_or_keyword']:
        if param.default == param.empty:
            this_kind = 'positional_or_keyword'
        else:
            this_kind = 'keyword1'
    elif param.kind in kinds['var_positional']:
        this_kind = 'var_positional'
    elif param.kind in kinds['keyword_only']:
        this_kind = 'keyword_only'
    else:
        raise ValueError('This kind of argument is not allowed.')

    if this_kind < prev_kind:
        raise ValueError('This should not happen.')

    return this_kind
