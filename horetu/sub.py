from .one import one

def sub(subparsers, fs):
    g = {}
    for f in fs:
        sp = subparsers.add_parser(f.__name__)
        g[f.__name__] = one(sp, f)
    return g

def nest(subparsers, x):
    output = {}
    for dest, y in x.items():
        if isinstance(y, dict):
            subsubparsers = subparsers.add_parser(dest = dest)
            output[dest] = nest(subsubparsers, y)
        elif isinstance(y, list):
            output[dest] = sub(subparsers, y)
        else:
            raise TypeError
    return output
