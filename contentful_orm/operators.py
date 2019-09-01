def field_query_factory(operator=None, **kwargs):
    params = dict()
    for key, val in kwargs.items():
        if operator is not None:
            params['fields.' + key + '[' + operator + ']'] = val
        else:
            params['fields.' + key] = val
    return params

def all_(**kwargs):
    return field_query_factory(operator='all', **kwargs)

def ne_(**kwargs):
    return field_query_factory(operator='ne', **kwargs)

def nin_(**kwargs):
    return field_query_factory(operator='nin', **kwargs)

def exists_(**kwargs):
    return field_query_factory(operator='exists', **kwargs)

def lt_(**kwargs):
    return field_query_factory(operator='lt', **kwargs)

def lte_(**kwargs):
    return field_query_factory(operator='lte', **kwargs)

def gt_(**kwargs):
    return field_query_factory(operator='gt', **kwargs)

def gte_(**kwargs):
    return field_query_factory(operator='gte', **kwargs)

def match_(**kwargs):
    return field_query_factory(operator='match', **kwargs)

def near_(**kwargs):
    return field_query_factory(operator='near', **kwargs)

def within_(**kwargs):
    return field_query_factory(operator='within', **kwargs)

def select(value):
    return {'select' : value}

def limit(value):
    return {'limit' : value}

def skip(value):
    return {'skip' : value}

def links_to_entry(entry_id):
    return {'links_to_entry' : entry_id}

def links_to_asset(asset_id):
    return {'links_to_asset' : asset_id}

def order(attribute):
    return {'order' : attribute}

def mimetype_group(mimetype_group):
    valid_groups = ['attachment', 'plaintext', 'image', 'audio', 'video', 'richtext', 'presentation', 'spreadsheet', 'pdfdocument', 'archive', 'code', 'markup']
    if mimetype_group not in valid_groups:
        raise ValueError('mimetype_group must be one of the following: ' + str(valid_groups))
    return {'mimetype_group' : mimetype_group}

def locale(locale):
    return {'locale' : locale}
