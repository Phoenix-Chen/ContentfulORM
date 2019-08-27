def query_factory(operator=None, **kwargs):
    params = dict()
    for key in kwargs.keys():
        params[key + '[' + operator + ']'] = kwargs[key]
    return params

def all_(**kwargs):
    return query_factory(operator='all', **kwargs)
