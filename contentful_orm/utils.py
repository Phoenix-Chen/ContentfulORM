import re

def generate_id(name: str) -> str:
    """Generate id in camelCase based on input.

        Args:
            name (str): input string.

        Returns:
            str : Generated id.

    """
    if name == '' or name == None:
        raise ValueError('Name cannot be empty or None.')

    if not re.match('^[a-zA-Z0-9_ ]+$', name):
        raise ValueError('Name can only contain alphabets, numbers, space and underscore.')

    if not name[0].isalpha():
        raise ValueError('Name can only start with alphabet.')

    # Split by space and underscore
    name.replace(' ', '_')
    id = ''.join([i.capitalize() for i in name.split('_')])
    return id[0].lower() + id[1:]


def _get_class_attr(cls) -> list:
    """Get all non-callable class attributes.

        Args:
            cls (type) : class.

        Returns:
            list : all non-callable class attributes.

    """
    return [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")]
