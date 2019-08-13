from .. import models
from .validations import LinkContentType
from ..utils import camel_case, _get_class_attr, _is_base_cls_type


class Field:
    def __init__(self, disabled: bool = False, localized: bool = False, omitted: bool = False, required: bool = False, validations: list = None):
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
        self.id = camel_case(name)

    def serialize(self):
        field = {}
        for attr in _get_class_attr(self):
            val = self.__getattribute__(attr)
            field[attr] = val
        return field

    def _to_items(self):
        """Help function to parse Field into items for ArrayField.
        """
        fields = self.serialize()
        del fields['name']
        del fields['id']
        del fields['disabled']
        del fields['localized']
        del fields['omitted']
        del fields['required']
        return fields


class SymbolField(Field):
    type = 'Symbol'


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
    def __init__(self, model_set: set = {}, error_msg: str = '', disabled: bool = False, localized: bool = False, omitted: bool = False, required: bool = False, validations: list = None):
        # Damn you first-class object
        if validations == None:
            validations = list()

        link_content_types = list()
        # Check if model_set contains only Model based class
        for model in model_set:
            if not _is_base_cls_type(model, models.Model):
                raise TypeError('model_set can only contain models.Model based class. Detected: ' + str(model) + '.')
            link_content_types.append(camel_case(model.__name__))

        self.type = 'Link'
        self.linkType = 'Entry'
        if len(link_content_types) > 0:
            validations.append(LinkContentType(link_content_types, error_msg=error_msg))

        super().__init__(disabled=disabled, localized=localized, omitted=omitted, required=required, validations=validations)


class DateField(Field):
    type = 'Date'


class ArrayField(Field):
    type = 'Array'
    items = dict()

    def __init__(self, items, disabled: bool = False, localized: bool = False, omitted: bool = False, required: bool = False, validations: list = None):
        if type(items) not in [SymbolField, ReferenceField, MediaField]:
            raise TypeError('ArrayField currently only accecpt SymbolField, ReferenceField and MediaField. Detected: ' + str(type(items)) + '.')
        self.items = items._to_items()
