class CustomMeta(type):
    def __new__(mcs, name, bases, classdict, **kwargs):
        custom_attrs = {}

        for key, value in classdict.items():
            if not (key.startswith("__") and key.endswith("__")):
                key = "custom_" + key
            custom_attrs[key] = value
        custom_attrs["__setattr__"] = mcs.__custom_setattr
        cls = super().__new__(mcs, name, bases, custom_attrs, **kwargs)
        return cls

    def __custom_setattr(cls, name, value):
        if not (name.startswith("__") and name.endswith("__")):
            name = "custom_" + name
        cls.__dict__[name] = value
