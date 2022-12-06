import types
from django.contrib.auth.models import User

from scanorm.inspector import get_module, get_models

from tests.blog.article.models import Article, Comment


class TestGetModule:
    """Tests function get_module"""

    def test_should_return_false_and_none_when_namespace_is_not_a_module(self):
        module_found, module = get_module('foobar')
        assert module_found is False
        assert module is None

    def test_should_return_true_and_module_when_namespace_is_a_module(self):
        module_found, module = get_module('django.contrib.sessions')
        assert module_found is True
        assert isinstance(module, types.ModuleType)


class TestGetModels:
    """Tests function get_models"""

    def test_should_yield_concrete_models_in_given_module(self):
        _, module = get_module('django.contrib.sessions')
        models = [item for item in get_models(module)]
        assert models == [
            ('User', User),
            ('Article', Article),
            ('Comment', Comment)
        ]
