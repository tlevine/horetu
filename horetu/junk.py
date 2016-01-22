
def aoeuaoeuaoeu_docs(f):
    '''
    I couldn't figure out how to use the docutils docstring parser, so I wrote
    my own. Can somebody show me the right way to do this?
    '''
    raise NotImplementedError
    from docutils.core import Publisher
    from docutils.io import StringInput
    pub = Publisher(None, None, None, settings=settings,
                    source_class=StringInput,
                    destination_class=destination_class)
    pub.set_components('standalone', 'restructuredtext', 'pseudoxml')
    pub.process_programmatic_settings(
        settings_spec, settings_overrides, config_section)
    pub.set_source(f.__doc__, f.__name__)
    pub.set_destination(None, f.__name__)
    output = pub.publish(enable_exit_status=False)
    return output, pub
    return publish_parts(f.__doc__, source_class=StringInput, source_path=f.__name__)
