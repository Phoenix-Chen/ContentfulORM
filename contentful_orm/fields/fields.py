import inspect
from json import JSONEncoder
from .. import models
from .validations import LinkContentType
from ..utils import generate_id


class Field:
    def __init__(self, disabled: bool = False, localized: bool = True, omitted: bool = False, required: bool = True, validations: list = None):
        self.name = None
        self.id = None
        self.disabled = disabled
        self.localized = localized
        self.omitted = omitted
        self.required = required
        # Damn you first-class object
        self.validations = [v.serialize() for v in validations] if validations != None else list()

    def set_name(self, name: str):
        """Set the name and the id of the field.
        """
        self.name = name
        self.id = generate_id(name)

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

# NOTE: Might change to use cls.__bases__ to verify base class
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

        if len(model_set) > 0:
            link_content_types = list()
            # Check if model_set contains only Model based class
            for model in model_set:
                if not is_base_cls_type(model, models.Model):
                    raise TypeError('model_set can only contain models.Model based class. Detected: ' + str(model) + '.')
                link_content_types.append(generate_id(model.__name__))


            validations.append(LinkContentType(link_content_types, error_msg=error_msg))

        super().__init__(disabled=disabled, localized=localized, omitted=omitted, required=required, validations=validations)
