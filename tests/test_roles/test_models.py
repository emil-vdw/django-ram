"""Test Roles app models."""
import pytest

from rest_iam.roles.models import Role
from tests.test_roles.models import CustomUser


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username="test_user")


@pytest.fixture
def role():
    return Role.objects.create(name="test role")


@pytest.mark.django_db
class TestRoleModel(object):
    def test_string_representation(self, role):
        assert str(role) == "test role"

    def test_add_user_role(self, role, user):
        assert role not in user.roles.all()
        user.roles.add(role)
        assert role in user.roles.all()


@pytest.mark.django_db
class TestRoleMixin(object):
    def test_has_role(self, user, role):
        assert user.has_role(role) is False
        user.roles.add(role)
        assert user.has_role(role)

    @pytest.mark.parametrize(
        "user_data_list,expected_usernames_with_role",
        [
            (
                [],
                set(),
            ),
            (
                [{"username": "test user 1"}],
                {"test user 1"},
            ),
            (
                [
                    {"username": "test user 1"},
                    {"username": "test user 2"},
                    {"username": "test user 3"},
                ],
                {"test user 1", "test user 2", "test user 3"},
            ),
        ],
    )
    def test_with_role(self, user_data_list, expected_usernames_with_role, role):
        for user_data in user_data_list:
            user = CustomUser.objects.create(**user_data)
            user.roles.set([role])

        assert (
            set(CustomUser.with_role(role).values_list("username", flat=True))
            == expected_usernames_with_role
        )
        assert (
            set(CustomUser.with_role(role.name).values_list("username", flat=True))
            == expected_usernames_with_role
        )
