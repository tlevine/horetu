from .one import one

def sub(parser, dest, fs):
    subparsers = parser.add_subparsers(dest = dest)
    g = {}
    for i, (k, f) in enumerate(fs.items()):
        sp = subparsers.add_parser(k)
        g[f.__name__] = one(sp, f)
        g[k] = f.__name__
    return g
