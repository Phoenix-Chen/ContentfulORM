import re
import inspect
from json import JSONEncoder

# class Validation:
#     def __init__(self, unique: bool = None):
#         self.validations = list()
#         # for arg in inspect.getfullargspec(self.__init__).args:
#         # print(inspect.getfullargspec(self.__init__))
#         if unique != None:
#             self.validations.append({'unique' : True})
#
#     # def valid_args(self):
#     #     """Validate the arguments passed are valid
#     #     """
#     #     pass
#
#     def __repr__(self):
#         return repr(self.validations)
#
# class ValidationEncoder(JSONEncoder):
#     def default(self, obj):
#         return obj.validations

def Validation(unique: bool = None):
    validations = list()
    if unique != None:
        validations.append({'unique' : True})
    return validations

class Field:
    def __init__(self, disabled: bool = False, localized: bool = True, omitted: bool = False, required: bool = True, validations: list = []):
        self.name = None
        self.id = None
        self.disabled = disabled
        self.localized = localized
        self.omitted = omitted
        self.required = required
        # self.validations = ValidationEncoder().encode(validations) if validations != None else []
        self.validations = validations

    def set_name(self, name: str):
        """Set the name and the id of the field.
        """
        self.name = name
        self.id = self._generate_id(name)


    def _generate_id(self, name: str) ->  str:
        """Generate field id based on field name.

            Args:
                name (str): Field name.

            Returns:
                str : Generated field id.

        """
        if name == '' or name == None:
            raise ValueError('Field name cannot be empty or None.')

        if not re.match('^[a-zA-Z0-9_ ]+$', name):
            raise ValueError('Field name can only contain alphabets, numbers, space and underscore.')

        if not name[0].isalpha():
            raise ValueError('Field name can only start with alphabet.')

        id = ''

        # Split by space and underscore
        name.replace(' ', '_')
        for i in name.split('_'):
            id += i.capitalize()
        return id[0].lower() + id[1:]


    def serialize(self):
        field = {}
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                val = self.__getattribute__(attr)
                field[attr] = val
        return field

class SymbolField(Field):
    type = 'Symbol'

class TextField(Field):
    type = 'Text'

class BooleanField(Field):
    type = 'Boolean'

class MediaField(Field):
    type = 'Link'
    linkType = 'Asset'

class IntegerField(Field):
    type = 'Integer'
