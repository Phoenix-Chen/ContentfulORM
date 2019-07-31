import inspect
from .fields import Field
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
    def serialize(self):
        attributes = dict()
        attributes['name'] = self.__class__.__name__
        attributes['description'] =  ''
        docstring = self.__class__.__doc__
        if docstring != None:
            attributes['description'] =  ' '.join(docstring.split())
        attributes['fields'] = list()
        for attr in dir(self):
            obj = getattr(self, attr)
            if not callable(obj) and not attr.startswith("__"):
                # Check if all attributes has Field based class
                if inspect.getmro(type(obj))[-2] != Field:
                    raise TypeError('Model fields must be a Field based class. Field (' + attr + ') is ' + str(type(obj)) + '.')
                obj.set_name(attr)
                attributes['fields'].append(obj.serialize())
        return attributes

    def create(self, connector):
        return connector.content_types().create(self.__id__, self.serialize())
