import importlib
import inspect
import json
import types
from pathlib import Path
from typing import Iterator, Optional, Type

from django.conf import settings
from django.db import models
from django.db.models.fields import Field


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


def get_model_fields(model: Type[models.Model]) -> Iterator[Field]:
    for field in model._meta.get_fields():
        yield field


def get_app_models(module: types.ModuleType) -> Optional[dict]:
    data = {}
    for name, model in get_models(module):
        data[name] = {}
        for field in get_model_fields(model):
            data[name][field.name] = field.__class__.__name__
    return data if data else None


def create_model_schema():
    schema = {}
    for app in settings.INSTALLED_APPS:
        parts: list[str] = app.split('.')

        # we handle django apps here
        if parts[0] == 'django':
            module_found, models_module = get_module(f'{app}.models')
            if not module_found:
                schema[app] = None
                continue
            schema[app] = get_app_models(models_module)

        # most user apps will be in the form "<app>.apps.<App>Config"
        elif len(parts) == 3 and parts[-1].endswith('Config'):
            module_found, models_module = get_module(f'{parts[0]}.models')
            if not module_found:
                schema[app] = None
                continue
            schema[app] = get_app_models(models_module)

        # some legacy apps used only the app name in settings
        elif len(parts) == 1:
            module_found, models_module = get_module(f'{parts[0]}.models')
            if not module_found:
                schema[app] = None
                continue
            schema[app] = get_app_models(models_module)
        else:
            schema[app] = None

    schema_path = Path(settings.BASE_DIR) / '.forestadmin-schema.json'
    with schema_path.open('w') as f:
        json.dump(schema, f)
