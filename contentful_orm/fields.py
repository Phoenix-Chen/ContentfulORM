import re
import inspect
from json import JSONEncoder
from . import models

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
    allowed_param = {
        'Symbol' : ['size']
    }
    validations = list()
    if unique != None:
        validations.append({'unique' : True})
    return validations

class Field:
    def __init__(self, disabled: bool = False, localized: bool = True, omitted: bool = False, required: bool = True, validations: list = None):
        self.name = None
        self.id = None
        self.disabled = disabled
        self.localized = localized
        self.omitted = omitted
        self.required = required
        # self.validations = ValidationEncoder().encode(validations) if validations != None else []
        # Damn you first-class object
        self.validations = validations if validations != None else list()

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

        # Split by space and underscore
        name.replace(' ', '_')
        id = ''.join([i.capitalize() for i in name.split('_')])
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

class DecimalField(Field):
    type = 'Number'

def is_base_cls_type(cls, target_base):
    """Check if target_base is cls's base class (besides object class)
    """
    # Check cls and target_base are classes instead of instance
    if type(cls) != type:
        raise TypeError('cls has to be a class, not ' + str(type(cls)) + '.')
    if type(target_base) != type:
        raise TypeError('target_base has to be a class, not ' + str(type(cls)) + '.')

    if inspect.getmro(cls)[-2] == target_base:
        return True
    return False

class ReferenceField(Field):
    type = 'Link'
    linkType = 'Entry'

    def __init__(self, model_set: set = {}, error_msg: str = '', disabled: bool = False, localized: bool = True, omitted: bool = False, required: bool = True, validations: list = None):
        # Damn you first-class object
        if validations == None:
            validations = list()
        link_content_type = dict()
        link_content_type['linkContentType'] = list()
        # Check if model_set contains only Model based class
        for model in model_set:
            if not is_base_cls_type(model, models.Model):
                raise TypeError('model_set can only contain models.Model based class. Detected: ' + str(model) + '.')
            link_content_type['linkContentType'].append(model.__id__)

        if error_msg != '' or None:
            link_content_type['message'] = error_msg

        # only add linkContentType if specified any entry type
        if len(link_content_type['linkContentType']) > 0:
            validations.append(link_content_type)

        super().__init__(disabled=disabled, localized=localized, omitted=omitted, required=required, validations=validations)
