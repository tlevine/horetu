from .one import one

def sub(subparsers, fs):
    g = {}
    for f in fs:
        sp = subparsers.add_parser(f.__name__)
        g[f.__name__] = one(sp, f)
    return g

def nest(subparsers, commands = [], subcommands = {}):
    if not isinstance(commands, list):
        raise TypeError('commands must be a list.')
    if not isinstance(subcommands, dict):
        raise TypeError('subcommands must be a dict.')

    output = sub(subparsers, commands)

    for dest, subcommand in subcommands.items():
        subparser = subparsers.add_parser(dest)
        if isinstance(subcommand, (list, dict)):
            subsubparsers = subparser.add_subparsers(dest = dest)
            output[dest] = nest(subsubparsers, commands = subcommand)
        else:
            output[dest] = one(subparser, subcommand)

    return output
