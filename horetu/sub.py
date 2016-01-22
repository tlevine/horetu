from .one import one

def sub(config_file, config_section, subparsers, fs):
    g = {}
    for f in fs:
        name = f.__name__
        sp = subparsers.add_parser(name)
        g[name] = one(config_file, config_section + ' ' + name, sp, f)
    return g

def nest(config_file, config_section,
         subparsers, commands = [], subcommands = {}):
    if not isinstance(commands, list):
        raise TypeError('commands must be a list.')
    if not isinstance(subcommands, dict):
        raise TypeError('subcommands must be a dict.')

    output = sub(config_file, config_section, subparsers, commands)

    for dest, subcommand in subcommands.items():
        subparser = subparsers.add_parser(dest)
        if isinstance(subcommand, dict):
            subsubparsers = subparser.add_subparsers(dest = dest)
            output[dest] = nest(config_file, config_section + ' ' + dest,
                                subsubparsers, subcommands = subcommand)
        elif hasattr(subcommand, '__call__'):
            output[dest] = one(config_file, config_section,
                               subparser, subcommand)
        else:
            raise TypeError

    return output
