import re
import inspect

def camel_case(s: str) -> str:
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
