import argparse
import inspect

from . import options

def horetu(f):
    '''
    :type f: Callable or dict
    :param f: The callable to produce the argument parser too,
        or a dict from str to callable to make subparsers.
    '''
    if hasattr(f, '__call__'):
        p = argparse.ArgumentParser(f.__name__, description = options.description(f),
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
        return _horetu_one(p, f)

def _horetu_one(parser, f):
    params = inspect.signature(f).parameters.values()
    helps = dict(options.docs(f))

    for param in params:
        if param.kind == param.VAR_KEYWORD:
            raise ValueError('Variable keyword args (**kwargs) are not allowed.')
        p.add_argument(options.name_or_flags(param), nargs = options.nargs(param),
                       type = options.argtype(param), choices = options.argchoices(param),
                       help = helps.get(param.name, ''), default = options.default(param))

    positional_arguments = [param.name for param in params if param.kind != param.VAR_KEYWORD]
    keyword_arguments = [param.name for param in params if param.kind == param.VAR_KEYWORD]

    def g(parsed_args):
        args = [getattr(parsed_args, attr) for attr in positional_arguments]
        kwargs = {attr:getattr(parsed_args, attr) for attr in keyword_arguments}
        return f(*args, **kwargs)
    if parser:
        return g
    else:
        return g(p.parse_args())

