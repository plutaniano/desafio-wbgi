from functools import wraps
from typing import Callable

_sentinel = object()


def computed_property(*attrs: str) -> Callable:
    cache = {}

    def decorator(func: Callable):
        @property
        @wraps(func)
        def decorated_func(self, *args, **kwargs):
            values = (getattr(self, attr, _sentinel) for attr in attrs)
            cache_key = tuple([self, *values])  # one cache per class instance

            if cache_key not in cache:
                cache[cache_key] = func(self, *args, **kwargs)

            return cache[cache_key]

        return decorated_func

    return decorator
