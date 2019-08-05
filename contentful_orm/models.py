import inspect
from .fields import fields
from functools import wraps

class Model:
    __id__ = None

    # class Decorators:
    #     @classmethod
    #     def has_id(func):
    #         @wraps(func)
    #         def _wrapper(*args, **kwargs):
    #             if args[0].__id__ == None:
    #                 raise ValueError('__id__ is a required attribute of Model.')
    #             return func(*args, **kwargs)
    #         return _wrapper
    #
    # @Decorators.has_id()
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
    def create(cls, connector):
        return connector.content_types().create(cls.__id__, cls.serialize())
