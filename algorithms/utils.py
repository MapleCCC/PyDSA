__all__ = ["decorate_all_methods"]

import inspect
import types


def decorate_all_methods(decorator):
    def decorate(cls):
        for name, func in inspect.getmembers(cls):
            if isinstance(func, types.FunctionType):
                setattr(cls, name, decorator(func))
        return cls
    return decorate
