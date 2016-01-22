def expand_dict_keys(x):
    for k, v in x.items():
        if hasattr(v, 'items'):
            for subk in expand_dict_keys(v):
                yield k + ' ' + subk
        else:
            yield k
