from .models import Model
from .utils import _is_base_cls_type, _get_class_attr

class ModelSerializer:
    class Meta:
        model = None
        fields = '__all__'

    def __init__(self, data, many=False):
        self.data = data
        self.many = many

        if self.Meta.model is None:
            raise NotImplementedError('Must assign Meta.model')
        if not _is_base_cls_type(self.Meta.model, Model):
            raise TypeError('Meta.model has to be a Model based class')

        all_fields = _get_class_attr(self.Meta.model)
        self.fields = None
        if self.Meta.fields == '__all__':
            self.fields = all_fields
        else:
            if type(self.Meta.fields) != list:
                raise TypeError('Meta.fields has to be either __all__ or a list or field names')
            for field_name in self.Meta.fields:
                if field_name not in all_fields:
                    raise ValueError('Field `' + str(field_name) + '` is not in Model `' + str(self.Meta.model.__name__) + '`')
            self.fields = self.Meta.fields

    def serialize(self):
        if self.many:
            l = list()
            for i in self.data:
                l.append(self._serialize_entry(i))
            return l
        else:
            return self._serialize_entry(self.data)

    def _serialize_entry(self, entry):
        d = dict()
        for field in self.fields:
            d[field] = entry.fields().get(field)
        return d
