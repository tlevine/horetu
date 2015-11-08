import argparse
import inspect
import re

from sphinx.util.docstrings import prepare_docstring

def description(f):
    try:
        return next(iter(prepare_docstring(f.__doc__)))
    except StopIteration:
        return ''

def horetu(f, parser = None):
    '''
    :param function f: The function to produce the argument parser too.
    '''
    params = inspect.signature(f).parameters.values()
    types = {k:v[0] for k,v in docs(f)}
    helps = {k:v[1] for k,v in docs(f)}

    if parser:
        p = parser
    else:
        p = argparse.ArgumentParser(f.__name__, description = description(f),
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    for param in params:
        if param.kind == param.VAR_KEYWORD:
            raise ValueError('Variable keyword args (**kwargs) are not allowed.')
        p.add_argument(name_or_flags(param), nargs = nargs(param), choices = choices(param),
                       type = types.get(param.name, str),
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

def docs(f):
    for line in prepare_docstring(f.__doc__):
        m = re.match(r'^:param ([^:]+ )?([^:]+): (.+)$', line)
        if m:
            k, *v = m.groups()
            yield k, v

def aoeuaoeuaoeu_docs(f):
    '''
    I couldn't figure out how to use the docutils docstring parser, so I wrote
    my own. Can somebody show me the right way to do this?
    '''
    raise NotImplementedError
    from docutils.core import Publisher
    from docutils.io import StringInput
    pub = Publisher(None, None, None, settings = settings,
                    source_class = StringInput,
                    destination_class = destination_class)
    pub.set_components('standalone', 'restructuredtext', 'pseudoxml')
    pub.process_programmatic_settings(
        settings_spec, settings_overrides, config_section)
    pub.set_source(f.__doc__, f.__name__)
    pub.set_destination(None, f.__name__)
    output = pub.publish(enable_exit_status = False)
    return output, pub
    return publish_parts(f.__doc__, source_class = StringInput, source_path = f.__name__)

def nargs(param):
    if param.kind == param.VAR_POSITIONAL:
        return '*'

def choices(param):
    if param.annotation == param.empty:
        return None
    else:
        return param.annotation

def name_or_flags(param):
    if param.default == param.empty:
        return param.name
    else:
        return '--' + param.name

def default(param):
    if param.default != param.empty:
        return param.default

