class Locale:
    @classmethod
    def _get_all(cls, connector):
        return connector.locales().all()

    @classmethod
    def _get_default(cls, connector):
        return cls._get_all(connector)[0].default_locale
