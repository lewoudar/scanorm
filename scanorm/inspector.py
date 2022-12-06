import importlib
import types
import inspect
from typing import Optional, Type, Iterator

from django.db import models


def get_module(namespace: str) -> tuple[bool, Optional[types.ModuleType]]:
    try:
        module = importlib.import_module(namespace)
    except (TypeError, ModuleNotFoundError):
        return False, None
    return True, module


def get_models(module: types.ModuleType) -> Iterator[tuple[str, Type[models.Model]]]:
    for member in inspect.getmembers(module):
        klass = member[1]
        if inspect.isclass(klass) and issubclass(klass, models.Model):
            if not klass._meta.abstract and not klass._meta.proxy:
                yield member
