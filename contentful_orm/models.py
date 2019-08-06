import inspect
from .fields import fields
from functools import wraps
from contentful_management.errors import NotFoundError
from .errors import OperationalError
from .utils import generate_id

# class Entry:
#     def __init__(self):
#         pass
#
#     def add_field(self, field_name, field_value):
#         pass

class Model:
    def __init__(self, **kwargs):
        fields = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        for key in kwargs.keys():
            if key not in fields:
                raise TypeError(str(type(self).__name__) + " got an unexpected keyword argument '" + key + "'")


    @classmethod
    def create(cls, connector):
        if cls.exist(connector):
            raise OperationalError('Content type ' + generate_id(cls.__name__) + ' already exist. Use update() to update fields.')
        return connector.content_types().create(generate_id(cls.__name__), cls.serialize())

    @classmethod
    def delete(cls, connector):
        if not cls.exist(connector):
            raise OperationalError('Content type ' + generate_id(cls.__name__) + ' does not exist.')
        return connector.content_types().delete(generate_id(cls.__name__))

    # @classmethod
    # def entries(cls, connector):
    #     if not cls.exist(connector):
    #         raise OperationalError('Content type ' + generate_id(cls.__name__) + ' does not exist.')
    #     content_type = cls.get_content_type(connector)
    #     return content_type.entries().all()

    @classmethod
    def exist(cls, connector):
        try:
            connector.content_types().find(generate_id(cls.__name__))
        except NotFoundError as nfe:
            return False
        return True

    @classmethod
    def get_content_type(cls, connector):
        return connector.content_types().find(generate_id(cls.__name__))

    @classmethod
    def publish(cls, connector):
        if not cls.exist(connector):
            raise OperationalError('Content type ' + generate_id(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(connector)
        return content_type.publish()

    @classmethod
    def serialize(cls):
        attributes = dict()
        attributes['name'] = cls.__name__
        attributes['description'] =  ''
        docstring = cls.__doc__
        if docstring != None:
            attributes['description'] =  ' '.join(docstring.split())
        attributes['fields'] = list()
        for attr in dir(cls):
            obj = getattr(cls, attr)
            if not callable(obj) and not attr.startswith("__"):
                # Check if all attributes has Field based class
                if inspect.getmro(type(obj))[-2] != fields.Field:
                    raise TypeError('Model fields must be a Field based class. Field (' + attr + ') is ' + str(type(obj)) + '.')
                obj.set_name(attr)
                attributes['fields'].append(obj.serialize())
        return attributes

    @classmethod
    def unpublish(cls, connector):
        if not cls.exist(connector):
            raise OperationalError('Content type ' + generate_id(cls.__name__) + ' does not exist.')
        content_type = cls.get_content_type(connector)
        return content_type.unpublish()
