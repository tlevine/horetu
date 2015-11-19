from .one import one

def sub(subparsers, fs):
    g = {}
    for f in fs:
        sp = subparsers.add_parser(f.__name__)
        g[f.__name__] = one(sp, f)
    return g

def nest(subparsers, commands = [], subcommands = {}):
    output = sub(subparsers, commands)

    for dest, subcommand in subcommands.items():
        subparser = subparsers.add_parser(dest)
        subsubparsers = subparser.add_subparsers(dest = dest)
        output[dest] = nest(subsubparsers, subcommand)

    return output
