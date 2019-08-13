def _get_all(connector):
    return connector.locales().all()

def get_default_code(connector):
    return _get_all(connector)[0].default_locale

def make_localizer(code):
    class Localizer:
        locale_code = code
        def __init__(self, data):
            self.data = data
        def localize(self):
            return {self.locale_code : self.data}
    return Localizer
