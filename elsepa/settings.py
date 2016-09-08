from functools import (reduce)
from copy import (copy)
from collections import OrderedDict


class TemporaryEntry(object):
    def __init__(self, settings, key):
        self._d = settings
        self._k = key

    def __getattr__(self, k):
        return TemporaryEntry(self._d, self._k + '.' + k)

    def __setattr__(self, k, v):
        if k[0] != '_':
            self._d[self._k + '.' + k] = v
        else:
            self.__dict__[k] = v

    def __bool__(self):
        return False

    def __contains__(self, k):
        return False


class Settings(OrderedDict):
    """A dictionary with additional additional accessability.
    Behaviour of a `Settings` object should mimic Javascript.
    The keys of the dictionary are restricted to be strings.
    """
    def __init__(self, _data=None, **kwargs):
        if _data:
            super(Settings, self).__init__(_data)
        else:
            super(Settings, self).__init__()
        for k, v in kwargs.items():
            self[k] = v

    def __setitem__(self, k, v):
        def get_or_create(d, k):
            if k not in d:
                super(Settings, d).__setitem__(k, Settings())
            return super(Settings, d).__getitem__(k)

        if type(v) is dict:
            v = Settings(v)

        keys = k.split('.')
        lowest_obj = reduce(get_or_create, keys[:-1], self)
        OrderedDict.__setitem__(lowest_obj, keys[-1], v)

    def __getitem__(self, k):
        keys = k.split('.')
        obj = reduce(OrderedDict.__getitem__, keys, self)
        return obj

    def __getattr__(self, k):
        if k not in self:
            return TemporaryEntry(self, k)

        return self[k]

    def __setattr__(self, k, v):
        if type(v) is dict:
            v = Settings(**v)

        self[k] = v


class Type(object):
    """The type of a single setting.

    .. :py:attribute:: description
        (str) Describing the meaning of the setting.

    .. :py:attribute:: default
        (any) Default value of the setting.

    .. :py:attribute:: check
        (any -> bool) A function that checks the validity
        of a setting.

    .. :py:attribute:: obligatory
        (bool) Is the parameter obligatory?

    .. :py:attribute:: transformer
        (any -> str) A function that transforms the value into a string
        suitable for this application. By default the `__str__` method
        (usual Python print method) is used.
    """
    def __init__(self, description, default=None, check=None,
                 obligatory=False, transformer=lambda x: x):
        self.description = description
        self.default = default
        self.check = check
        self.obligatory = obligatory
        self.transformer = transformer


class Model(Settings):
    """Settings can be matched against a template to check correctness of
    data types and structure etc. At the same time the template can act as
    a way to create default settings."""
    def __init__(self, _data=None, **kwargs):
        super(Model, self).__init__(**kwargs)
        if _data is not None:
            for k, v in _data:
                self[k] = v

    def __setitem__(self, k, v):
        if isinstance(v, Model):
            return super(Model, self).__setitem__(k, v)

        if isinstance(v, Type):
            return super(Model, self).__setitem__(k, v)

        if isinstance(v, dict):
            return super(Model, self).__setitem__(k, Model(**v))

        raise TypeError(
            "Model object can only contain Model "
            "or Type: got {}".format(v))


def check_settings(s: Settings, d: Model):
    for k, v in s.items():
        if not d[k].check(v):
            raise TypeError(
                    "Type-check for setting `{}` failed: {}".format(k, v))
    return True


def apply_defaults_and_check(s: Settings, d: Model):
    s = Settings(**s)

    for k in d:
        if k not in s:
            if isinstance(d[k], Model):
                s[k] = Settings()
            elif d[k].obligatory:
                raise Exception("Setting `{}` is obligatory but was not"
                                " given.".format(k))
            else:
                s[k] = copy(d[k].default)

        if isinstance(d[k], Model):
            if not isinstance(s[k], Settings):
                raise TypeError(
                    "Sub-folder {} of settings should be a collection."
                    .format(k))
            s[k] = apply_defaults_and_check(s[k], d[k])

        if not d[k].check(s[k]):
            raise TypeError(
                    "Type-check for setting `{}` failed: {}".format(k, s[k]))

    return s
