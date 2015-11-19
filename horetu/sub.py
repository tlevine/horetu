from .one import one

def sub(subparsers, fs):
    g = {}
    for f in fs:
        sp = subparsers.add_parser(f.__name__)
        g[f.__name__] = one(sp, f)
    return g

def nest(subparsers, x):
    if isinstance(x, dict):
        output = {}
        for dest, y in x.items():
            subparser = subparsers.add_parser(dest)
            subsubparsers = subparser.add_subparsers(dest = dest)
            output[dest] = nest(subsubparsers, y)
    elif isinstance(x, list):
        return sub(subparsers, x)
    else:
        raise TypeError
    return output
