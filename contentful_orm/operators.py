def query_factory(operator=None, **kwargs):
    params = dict()
    for key in kwargs.keys():
        params[key + '[' + operator + ']'] = kwargs[key]
    return params

def all_(**kwargs):
    return query_factory(operator='all', **kwargs)

def ne_(**kwargs):
    return query_factory(operator='ne', **kwargs)

def nin_(**kwargs):
    return query_factory(operator='nin', **kwargs)

def exists_(**kwargs):
    return query_factory(operator='exists', **kwargs)

def lt_(**kwargs):
    return query_factory(operator='lt', **kwargs)

def lte_(**kwargs):
    return query_factory(operator='lte', **kwargs)

def gt_(**kwargs):
    return query_factory(operator='gt', **kwargs)

def gte_(**kwargs):
    return query_factory(operator='gte', **kwargs)

def match_(**kwargs):
    return query_factory(operator='match', **kwargs)

def near_(**kwargs):
    return query_factory(operator='near', **kwargs)

def within_(**kwargs):
    return query_factory(operator='within', **kwargs)
