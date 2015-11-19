from .one import one

def sub(parser, dest, fs):
    subparsers = parser.add_subparsers(dest = dest)
    g = {}
    for f in fs:
        sp = subparsers.add_parser(f.__name__)
        g[f.__name__] = one(sp, f)
    return g

def nest(parser, x):
    for dest, y in x.items():
        if isinstance(y, dict):
            subparsers = parser.add_subparsers(dest = dest)
            for subdest, z in subparsers.items():
                subparser = subparsers.add_parser(dest = subdest)
                nest(parser, z)

        elif isinstance(y, list):
            sub(parser, dest, y)
        else:
            raise TypeError
