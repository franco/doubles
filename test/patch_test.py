import pytest

from doubles import patch, patch_constructor, InstanceDoubleFactory, InstanceDouble
from doubles.lifecycle import teardown
from doubles.exceptions import VerifyingDoubleImportError
import doubles.testing


class TestPatch(object):
    def test_patch_with_no_new_object_supplied(self):
        original_value = doubles.testing.User
        patch_constructor('doubles.testing.User')

        assert isinstance(doubles.testing.User, InstanceDoubleFactory)
        assert not original_value == doubles.testing.User

    def test_patch_wth_new_object_supplied(self):
        patch('doubles.testing.User', 'Bob Barker')

        assert doubles.testing.User == 'Bob Barker'

    def test_restores_original_value(self):
        original_value = doubles.testing.User
        patch('doubles.testing.User')

        teardown()

        assert original_value == doubles.testing.User

    def test_patch_objects_value(self):
        p = patch('doubles.testing.User', 'Bob Barker')

        assert doubles.testing.User == p.value

    def test_patched_objects_constructor_returns_instance_double(self):
        patch_constructor('doubles.testing.User')

        user = doubles.testing.User()
        assert isinstance(user, InstanceDouble)

    def test_raises_an_error_trying_to_patch_a_function(self):
        with pytest.raises(VerifyingDoubleImportError):
            patch_constructor('doubles.test.top_level_function')

    def test_using_the_patched_class(self):
        patch_constructor('doubles.testing.User')
        patch_constructor('doubles.testing.OldStyleUser')

        result_1, result_2 = doubles.testing.top_level_function_that_creates_an_instance()

        assert isinstance(result_1, InstanceDouble)
        assert isinstance(result_2, InstanceDouble)