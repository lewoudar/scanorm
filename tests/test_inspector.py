import types
from scanorm.inspector import get_module, get_models


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
