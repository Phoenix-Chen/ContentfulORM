import inspect
from .fields import Field

class Model:
    def to_schema(self):
        attributes = dict()
        attributes['name'] = self.__class__.__name__
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

    def generate_id(self):
        pass
