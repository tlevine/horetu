import re
from collections import Counter
from functools import partial
import operator

from . import options
from . import annotations

FLAG = re.compile(r'^-?(-[^-]).*')

def one(parser, f):
    params = annotations.params(f)
    helps = dict(options.docs(f))
    has_keyword_only = options.has_keyword_only(params)
    get_name_or_flag = partial(options.name_or_flag, has_keyword_only)

    matches = map(partial(re.match, FLAG), map(get_name_or_flag, params))
    single_character_flags = Counter(m.group(1) for m in matches if m)
    single_character_flags['-h'] += 1

    for i, param in enumerate(params):
        if param.kind == param.VAR_KEYWORD:
            raise ValueError('Variable keyword args (**kwargs) are not allowed. You may implement your own key-value parser that takes the result of variable positional args (*args).')
        name_or_flag = get_name_or_flag(param)
        m = re.match(FLAG, name_or_flag)
        if m and single_character_flags[m.group(1)] == 1:
            args = (name_or_flag, m.group(1))
        else:
            args = name_or_flag,
        kwargs = dict(nargs = options.nargs(has_keyword_only, param),
                      action = options.action(param),
                      dest = options.dest(param),
                      type = options.argtype(param),
                      choices = options.argchoices(param),
                      help = helps.get(param.name, ''),
                      default = options.default(param))
        if kwargs['action'] in {'store_true', 'store_false', 'count'}:
            del(kwargs['choices'])
            del(kwargs['type'])
            del(kwargs['nargs'])
        if not name_or_flag.startswith('-'):
            del(kwargs['dest'])
        parser.add_argument(*args, **kwargs)

    def g(parsed_args):
        args = [getattr(parsed_args, attr) for attr in _get_args(False, params)]
        for param in params:
            if param.kind == param.VAR_POSITIONAL:
                args.extend(getattr(parsed_args, param.name))
        kwargs = {attr:getattr(parsed_args, attr) for attr in _get_args(True, params)}
        return f(*args, **kwargs)
    return g

def _get_args(keyword, params):
    if keyword:
        comparator = operator.eq
    else:
        comparator = operator.ne
    return [param.name for param in params if comparator(param.kind, param.VAR_KEYWORD) and param.kind != param.VAR_POSITIONAL]
