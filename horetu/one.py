import re
from collections import Counter
from functools import partial
import inspect

from . import options

FLAG = re.compile(r'^-?(-[^-]).*')

def one(parser, f):
    params = inspect.signature(f).parameters.values()
    helps = dict(options.docs(f))

    matches = map(partial(re.match, FLAG), map(options.name_or_flags, params))
    single_character_flags = Counter(m.group(1) for m in matches if m)

    for i, param in enumerate(params):
        if param.kind == param.VAR_KEYWORD:
            raise ValueError('Variable keyword args (**kwargs) are not allowed.')
        name_or_flag = options.name_or_flags(param)
        m = re.match(FLAG, name_or_flag)
        if m and single_character_flags[m.group(1)] == 1:
            name_or_flags = (name_or_flag, m.group(1))
        else:
            name_or_flags = name_or_flag,
        parser.add_argument(*name_or_flags, nargs = options.nargs(param),
                            type = options.argtype(param), choices = options.argchoices(param),
                            help = helps.get(param.name, ''), default = options.default(param))

    positional_arguments = [param.name for param in params if param.kind != param.VAR_KEYWORD]
    keyword_arguments = [param.name for param in params if param.kind == param.VAR_KEYWORD]

    def g(parsed_args):
        args = [getattr(parsed_args, attr) for attr in positional_arguments]
        kwargs = {attr:getattr(parsed_args, attr) for attr in keyword_arguments}
        return f(*args, **kwargs)
    return g
