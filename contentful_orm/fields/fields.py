from .. import models
from .validations import LinkContentType
from ..utils import generate_id, _get_class_attr, _is_base_cls_type


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
        for attr in _get_class_attr(self):
            val = self.__getattribute__(attr)
            field[attr] = val
        return field

# NOTE: add class ArrayField

class SymbolField(Field):
    type = 'Symbol'
    def __init__(self, many: bool = False, disabled: bool = False, localized: bool = True, omitted: bool = False, required: bool = True, validations: list = None):
        if validations == None:
            validations = list()

        if many:
            self.type = 'Array'
            self.items = dict()
            self.items['type'] = 'Symbol'
            self.items['validations'] = validations

        super().__init__(disabled=disabled, localized=localized, omitted=omitted, required=required, validations=None)

class TextField(Field):
    type = 'Text'


class RichTextField(Field):
    type = 'RichText'


class BooleanField(Field):
    type = 'Boolean'


class MediaField(Field):
    type = 'Link'
    linkType = 'Asset'


class IntegerField(Field):
    type = 'Integer'


class DecimalField(Field):
    type = 'Number'


class ReferenceField(Field):
    def __init__(self, model_set: set = {}, many: bool = False, error_msg: str = '', disabled: bool = False, localized: bool = True, omitted: bool = False, required: bool = True, validations: list = None):
        # Damn you first-class object
        if validations == None:
            validations = list()

        link_content_types = list()
        # Check if model_set contains only Model based class
        for model in model_set:
            if not _is_base_cls_type(model, models.Model):
                raise TypeError('model_set can only contain models.Model based class. Detected: ' + str(model) + '.')
            link_content_types.append(generate_id(model.__name__))

        if many:
            self.type = 'Array'
            self.items = dict()
            self.items['type'] = 'Link'
            self.items['linkType'] = 'Entry'
            self.items['validations'] = list()
            if len(model_set) > 0:
                self.items['validations'].append(LinkContentType(link_content_types, error_msg=error_msg).serialize())
        else:
            self.type = 'Link'
            self.linkType = 'Entry'
            if len(model_set) > 0:
                validations.append(LinkContentType(link_content_types, error_msg=error_msg))

        super().__init__(disabled=disabled, localized=localized, omitted=omitted, required=required, validations=validations)


class DateField(Field):
    type = 'Date'
