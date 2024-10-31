from collections.abc import Callable
from functools import wraps
from typing import Any, Tuple

_sentinel = object()


def computed_property(*attrs: str) -> Callable[..., property]:
    def decorator(func: Callable[[Callable[..., Any]], property]):
        cache: dict[Tuple[Any, ...], Any] = {}

        @property
        @wraps(func)
        def decorated_func(self: Any, *args: Any, **kwargs: Any) -> Any:
            cache_key = tuple(getattr(self, attr, _sentinel) for attr in attrs)

            if cache_key not in cache:
                cache[cache_key] = func(self, *args, **kwargs)

            return cache[cache_key]

        return decorated_func

    return decorator
