import re
import inspect
import uuid
from baseconv import base62

def camel_case(s):
    """Generate id in camelCase based on input.

        Args:
            s (str): input string.

        Returns:
            str : Generated id.

    """
    if s == '' or s == None:
        raise ValueError('Input cannot be empty or None.')
    if not re.match('^[a-zA-Z0-9_ ]+$', s):
        raise ValueError('Input can only contain alphabets, numbers, space and underscore.')
    if not s[0].isalpha():
        raise ValueError('Input can only start with alphabet.')
    # Split by space and underscore
    s.replace(' ', '_')
    cs = ''.join([i.capitalize() for i in s.split('_')])
    return cs[0].lower() + cs[1:]

def _get_class_attr(cls) -> list:
    """Get all non-callable class attributes.

        Args:
            cls (type) : class.

        Returns:
            list : all non-callable class attributes.

    """
    return [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]

# NOTE: Might change to use cls.__bases__ to verify base class
def _is_base_cls_type(cls, target_base):
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

def generate_id():
    """Generate 128 bit UUID encoded in base 62

        See: https://www.contentfulcommunity.com/t/support-for-standard-uuids/1635

        Returns:
            str : generated ID.
    """
    uuid_hex = str(uuid.uuid4()).replace('-','')
    uuid_int = int(uuid_hex, 16)
    return base62.encode(uuid_int)

def _validate_regex_flags(flags: str):
    """Check if input flags are valid.
    """
    allowed_flags = {'g', 'i', 'm', 's', 'u', 'y'}
    for char in flags:
        if char in allowed_flags:
            allowed_flags.remove(char)
        else:
            raise ValueError('Invalid flags. see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp for more details.')
