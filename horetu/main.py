import argparse
import inspect

from . import options

def horetu(f, parser = None):
    '''
    :param function f: The function to produce the argument parser too.
    '''
    params = inspect.signature(f).parameters.values()
    helps = dict(docs(f))

    if parser:
        p = parser
    else:
        p = argparse.ArgumentParser(f.__name__, description = util.description(f),
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    for param in params:
        if param.kind == param.VAR_KEYWORD:
            raise ValueError('Variable keyword args (**kwargs) are not allowed.')
        p.add_argument(name_or_flags(param), nargs = nargs(param), type = argtype(param),
                       choices = argchoices(param),
                       help = helps.get(param.name, ''), default = default(param))

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

