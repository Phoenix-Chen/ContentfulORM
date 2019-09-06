import re
from contentful_management.content_type_entries_proxy import ContentTypeEntriesProxy
from .operators import field_query_factory


class ORMContentTypeEntriesProxy(ContentTypeEntriesProxy):
    @classmethod
    def from_parent(cls, parent, content_type_fields):
        return cls(parent.proxy.client, parent.proxy.space_id, parent.proxy.environment_id, parent.proxy.content_type_id, content_type_fields)

    def __init__(self, client, space_id, environment_id, content_type_id, content_type_fields):
        super().__init__(client, space_id, environment_id, content_type_id)
        self.content_type_fields = content_type_fields

    def _get_field_name(self, param):
        """Return field name from query parameter by split '.' and '['
        """
        return re.split('\.|\[', param)[1]

    # Currently doesn't support relational queries
    def _make_queries(self, fields, kw_dict):
        queries = dict()
        for key, val in kw_dict.items():
            # Check if the query param is field query
            if key[:7] == 'fields.':
                field_name = self._get_field_name(key)
                if field_name not in fields.keys():
                    raise TypeError(str(self.proxy.content_type_id) + " does not contain field: '" + key + "'")
                queries['fields.' + fields[field_name] + key[7 + len(field_name):]] = val
            else:
                queries[key] = val
        return queries

    def filter(self, *args, **kwargs):
        fields_name_id = self.get_fields_name_id()
        queries = dict()
        for arg in args:
            queries.update(self._make_queries(fields_name_id, arg))
        queries.update(self._make_queries(fields_name_id, field_query_factory(**kwargs)))
        return self.all(query=queries)

    def get_fields_name_id(self):
        """Return a dict of field name to field ID.
        """
        fields_name_id = dict()
        for i in self.content_type_fields:
            fields_name_id[i.name] = i._real_id()
        return fields_name_id
