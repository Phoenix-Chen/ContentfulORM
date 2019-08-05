class Validation:
    def __init__(self, error_msg: str = ''):
        self.message = error_msg

    def serialize(self):
        field = {}
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                val = self.__getattribute__(attr)
                field[attr] = val
        return field


class Range(Validation):
    def __init__(self, max: float = None, min: float = None, error_msg: str = ''):
        if max == None and min == None:
            raise TypeError('Range requires argument max or min or both.')
        self.range = dict()
        if max != None:
            self.range['max'] = max
        if min != None:
            self.range['min'] = min


class Size(Validation):
    def __init__(self, max: float = None, min: float = None, error_msg: str = ''):
        if max == None and min == None:
            raise TypeError('Size requires argument max or min or both.')
        self.size = dict()
        if max != None:
            self.size['max'] = max
        if min != None:
            self.size['min'] = min


class In(Validation):
    def __init__(self, values: list, error_msg: str = ''):
        self.__in__ = list()
        if values != None:
            self.__in__ = values
        super().__init__(error_msg=error_msg)

    # Since in is python keyword
    def serialize(self):
        validations = super().serialize()
        validations['in'] = self.__in__
        return validations


class LinkContentType(Validation):
    def __init__(self, link_content_types: list, error_msg: str = ''):
        self.linkContentType = link_content_types
        super().__init__(error_msg=error_msg)

class Unique:
    @staticmethod
    def serialize():
        return {'unique' : True}
