from contentful_management.environment import Environment

class ORMEnvironment(Environment):
    @classmethod
    def from_parent(cls, env):
        return cls(env.raw, default_locale=env.default_locale, client=env._client)

    def __init__(self, item, **kwargs):
        super().__init__(item, **kwargs)

    def create(self, obj):
        return obj.create(self)

    def delete(self, obj):
        return obj.delete(self)

    def update(self, obj):
        return obj.update(self)

    def publish(self, obj):
        return obj.publish(self)

    def unpublish(self, obj):
        return obj.unpublish(self)

    def query(self, model):
        return model.query(self)

    def add(self, obj, id: str = None):
        return obj.add(self, id=id)
