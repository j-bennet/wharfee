# -*- coding: utf-8
import functools


def if_exception_return(ex_type, then_result):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except ex_type as x:
                self.exception = x
                return then_result
        return wrapper
    return decorator
