from .one import one

def sub(parser, dest, fs):
    subparsers = parser.add_subparsers(dest = dest)
    g = {}
    for f in fs:
        sp = subparsers.add_parser(f.__name__)
        g[f.__name__] = one(sp, f)
    return g
