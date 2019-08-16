import inspect
from .fields import fields
from functools import wraps
from contentful_management.errors import NotFoundError
from contentful_management.content_type_entries_proxy import ContentTypeEntriesProxy
from .errors import OperationalError
from .utils import camel_case, _get_class_attr, generate_id
from .locales import get_default_code, make_localizer

class ORMContentTypeEntriesProxy(ContentTypeEntriesProxy):
    @classmethod
    def from_parent(cls, parent, content_type_fields):
        return cls(parent.proxy.client, parent.proxy.space_id, parent.proxy.environment_id, parent.proxy.content_type_id, content_type_fields)

    def __init__(self, client, space_id, environment_id, content_type_id, content_type_fields):
        super().__init__(client, space_id, environment_id, content_type_id)
        self.content_type_fields = content_type_fields

    def filter(self, **kwargs):
        fields_name_id = self.get_fields_name_id()
        query = {}
        for key in kwargs.keys():
            if key not in fields_name_id.keys():
                raise TypeError(str(self.proxy.content_type_id) + " does not contain field: '" + key + "'")
            query['fields.' + fields_name_id[key] + '[all]'] = kwargs[key]
        return self.all(query=query)

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

    def to_entry(self, connector):
        default_localizer = make_localizer(get_default_code(connector))
        # Check if each field is localized
        for field_name in self.__entry__['fields'].keys():
            # If not localized use default locale
            # Currently no cleaner soluiton other than string compare
            if str(type(self.__entry__['fields'][field_name])) != str(default_localizer):
                self.__entry__['fields'][field_name] = default_localizer(self.__entry__['fields'][field_name])
            self.__entry__['fields'][field_name] = self.__entry__['fields'][field_name].localize()
        return self.__entry__

    def add(self, connector, id: str = None):
        if id == None:
            id = generate_id()
        # NOTE: considering check id duplication
        # Although generate_id is UUID and contentful_management should handle duplicate id problem
        return connector.entries().create(id, self.to_entry(connector))

    @classmethod
    def create(cls, connector):
        if cls.exist(connector):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' already exist. Use update() to update fields.')
        return connector.content_types().create(camel_case(cls.__name__), cls.serialize())

    @classmethod
    def delete(cls, connector):
        if not cls.exist(connector):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        return connector.content_types().delete(camel_case(cls.__name__))

    @classmethod
    def query(cls, connector):
        if not cls.exist(connector):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(connector)
        return ORMContentTypeEntriesProxy.from_parent(content_type.entries(), content_type.fields)

    @classmethod
    def exist(cls, connector):
        try:
            connector.content_types().find(camel_case(cls.__name__))
        except NotFoundError as nfe:
            return False
        return True

    @classmethod
    def get_content_type(cls, connector):
        return connector.content_types().find(camel_case(cls.__name__))

    @classmethod
    def publish(cls, connector):
        if not cls.exist(connector):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(connector)
        return content_type.publish()

    @classmethod
    def serialize(cls):
        # Enforce implement __display_field__
        if cls.__display_field__ == None:
            raise NotImplementedError("Must assign __display_field__")

        attributes = dict()
        attributes['name'] = cls.__name__
        attributes['description'] =  ''
        docstring = cls.__doc__
        if docstring != None:
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

        if attributes['displayField'] == None:
            raise ValueError('__display_field__ must be one of the attributes. `' + str(cls.__display_field__) + '` cannot be found.')
        return attributes

    @classmethod
    def unpublish(cls, connector):
        if not cls.exist(connector):
            raise OperationalError('Content type ' + camel_case(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(connector)
        return content_type.unpublish()
