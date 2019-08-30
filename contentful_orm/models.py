import inspect
import re
from .fields import fields
from functools import wraps
from contentful_management.errors import NotFoundError
from contentful_management.content_type_entries_proxy import ContentTypeEntriesProxy
from .errors import OperationalError
from .utils import camel_case, _get_class_attr, generate_id
from .locales import get_default_code, make_localizer
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


class Model:
    __display_field__ = None

    def __init__(self, **kwargs):
        self.__entry__ = dict()
        self.__entry__['content_type_id'] = camel_case(type(self).__name__)
        self.__entry__['fields'] = dict()
        fields = _get_class_attr(self)
        for key in kwargs.keys():
            if key not in fields:
                raise TypeError(str(type(self).__name__) + " got an unexpected keyword argument '" + key + "'")
            self.__entry__['fields'][camel_case(key)] = kwargs[key]

    def to_entry(self, env):
        default_localizer = make_localizer(get_default_code(env))
        # Check if each field is localized
        for field_name in self.__entry__['fields'].keys():
            # If not localized use default locale
            # Currently no cleaner soluiton other than string compare
            if str(type(self.__entry__['fields'][field_name])) != str(default_localizer):
                self.__entry__['fields'][field_name] = default_localizer(self.__entry__['fields'][field_name])
            self.__entry__['fields'][field_name] = self.__entry__['fields'][field_name].localize()
        return self.__entry__

    def add(self, env, id: str = None):
        if id is None:
            id = generate_id()
        # NOTE: considering check id duplication
        # Although generate_id is UUID and contentful_management should handle duplicate id problem
        # NOTE: add rollback if add fails
        return env.entries().create(id, self.to_entry(env))

    @classmethod
    def create(cls, env):
        if cls.exist(env):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' already exist. Use update() to update fields.')
        return env.content_types().create(camel_case(cls.__name__), cls.serialize())

    @classmethod
    def delete(cls, env):
        if not cls.exist(env):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        return env.content_types().delete(camel_case(cls.__name__))

    @classmethod
    def query(cls, env):
        if not cls.exist(env):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(env)
        return ORMContentTypeEntriesProxy.from_parent(content_type.entries(), content_type.fields)

    @classmethod
    def exist(cls, env):
        try:
            env.content_types().find(camel_case(cls.__name__))
        except NotFoundError as nfe:
            return False
        return True

    @classmethod
    def get_content_type(cls, env):
        return env.content_types().find(camel_case(cls.__name__))

    @classmethod
    def publish(cls, env):
        if not cls.exist(env):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(env)
        return content_type.publish()

    @classmethod
    def serialize(cls):
        # Enforce implement __display_field__
        if cls.__display_field__ is None:
            raise NotImplementedError("Must assign __display_field__")

        attributes = dict()
        attributes['name'] = cls.__name__
        attributes['description'] =  ''
        docstring = cls.__doc__
        if docstring is not None:
            attributes['description'] =  ' '.join(docstring.split())
        attributes['displayField'] = None
        attributes['fields'] = list()
        for attr in _get_class_attr(cls):
            obj = getattr(cls, attr)
            # Check if all attributes has Field based class
            if inspect.getmro(type(obj))[-2] != fields.Field:
                raise TypeError('Model fields must be a Field based class. Field (' + attr + ') is ' + str(type(obj)) + '.')
            obj.set_name(attr)
            # Check if __display_field__ is one of the attributes
            if cls.__display_field__ == attr:
                attributes['displayField'] = obj.id
            attributes['fields'].append(obj.serialize())

        if attributes['displayField'] is None:
            raise ValueError('__display_field__ must be one of the attributes. `' + str(cls.__display_field__) + '` cannot be found.')
        return attributes

    @classmethod
    def unpublish(cls, env):
        if not cls.exist(env):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(env)
        return content_type.unpublish()
