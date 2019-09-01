from ..utils import _validate_regex_flags

class Validation:
    def __init__(self, error_msg=''):
        self.message = error_msg

    def serialize(self):
        field = {}
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                val = self.__getattribute__(attr)
                field[attr] = val
        return field


class Range(Validation):
    def __init__(self, max=None, min=None, error_msg=''):
        if max is None and min is None:
            raise TypeError('Range requires argument max or min or both.')
        self.range = dict()
        if max is not None:
            self.range['max'] = max
        if min is not None:
            self.range['min'] = min
        super().__init__(error_msg=error_msg)


class Size(Validation):
    def __init__(self, max=None, min=None, error_msg=''):
        if max is None and min is None:
            raise TypeError('Size requires argument max or min or both.')
        self.size = dict()
        if max is not None:
            self.size['max'] = max
        if min is not None:
            self.size['min'] = min
        super().__init__(error_msg=error_msg)


class In(Validation):
    def __init__(self, values, error_msg=''):
        self.__in__ = list()
        if values is not None:
            self.__in__ = values
        super().__init__(error_msg=error_msg)

    # Since in is python keyword
    def serialize(self):
        validations = super().serialize()
        validations['in'] = self.__in__
        return validations


class LinkContentType(Validation):
    def __init__(self, link_content_types, error_msg=''):
        self.linkContentType = link_content_types
        super().__init__(error_msg=error_msg)


class Regex(Validation):
    def __init__(self, pattern, flags=None, error_msg=''):
        self.regexp = dict()
        self.regexp['pattern'] = pattern
        if flags is not None:
            _validate_regex_flags(flags)
            self.regexp['flags'] = flags
        super().__init__(error_msg=error_msg)


class ProhibitRegex(Validation):
    def __init__(self, pattern, flags=None, error_msg=''):
        self.prohibitRegexp = dict()
        self.prohibitRegexp['pattern'] = pattern
        if flags is not None:
            _validate_regex_flags(flags)
            self.prohibitRegexp['flags'] = flags
        super().__init__(error_msg=error_msg)


class ImageDimensions(Validation):
    def __init__(self, max_width=None, min_width=None, max_height=None, min_height=None, error_msg=''):
        if max_width is None and min_width is None and max_height is None and min_height is None:
            raise TypeError('ImageDimensions requires at least one of the arguments max_width, min_width, max_height or min_height.')
        self.assetImageDimensions = dict()
        self.assetImageDimensions['width'] = dict()
        self.assetImageDimensions['width']['max'] = max_width
        self.assetImageDimensions['width']['min'] = min_width
        self.assetImageDimensions['height'] = dict()
        self.assetImageDimensions['height']['max'] = max_height
        self.assetImageDimensions['height']['min'] = min_height
        super().__init__(error_msg=error_msg)


class FileSize(Validation):
    def __init__(self, max=None, min=None, error_msg=''):
        if max is None and min is None:
            raise TypeError('FileSize requires argument max or min or both.')
        self.assetFileSize = dict()
        if max is not None:
            self.assetFileSize['max'] = max
        if min is not None:
            self.assetFileSize['min'] = min
        super().__init__(error_msg=error_msg)


class Unique:
    @staticmethod
    def serialize():
        return {'unique' : True}
