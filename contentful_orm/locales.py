def _get_all(env):
    return env.locales().all()

def get_default_code(env):
    return _get_all(env)[0].default_locale

def make_localizer(code):
    class Localizer:
        locale_code = code
        def __init__(self, data):
            self.data = data
        def localize(self):
            return {self.locale_code : self.data}
    return Localizer
