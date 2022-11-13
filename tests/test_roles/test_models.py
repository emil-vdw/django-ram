"""Test Roles app models."""
import pytest

from django_ram.models import Role
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
    @pytest.mark.parametrize(
        "user_data,add_test_role,should_have_role",
        [
            (
                {
                    "is_active": True,
                    "is_superuser": True,
                },
                True,
                True,
            ),
            (
                {
                    "is_active": True,
                    "is_superuser": True,
                },
                False,
                True,
            ),
            (
                {
                    "is_active": False,
                    "is_superuser": True,
                },
                False,
                False,
            ),
            (
                {
                    "is_active": True,
                    "is_superuser": False,
                },
                True,
                True,
            ),
            (
                {
                    "is_active": True,
                    "is_superuser": False,
                },
                False,
                False,
            ),
        ],
    )
    def test_has_role(self, user_data, add_test_role, should_have_role, role):
        user = CustomUser.objects.create_user(username="test_user", **user_data)

        if add_test_role:
            user.roles.add(role)

        assert user.has_role(role) == should_have_role

    @pytest.mark.parametrize(
        "user_data_list,users_with_role,with_role_kwargs,expected_usernames_with_role",
        [
            ([], [], {}, []),
            (
                [{"username": "test user 1"}],
                ["test user 1"],
                {},
                ["test user 1"],
            ),
            (
                [
                    {"username": "test user 1"},
                    {"username": "test user 2"},
                    {"username": "test user 3"},
                ],
                ["test user 1", "test user 2", "test user 3"],
                {},
                ["test user 1", "test user 2", "test user 3"],
            ),
            (
                [
                    {"username": "test user 1"},
                    {"username": "test user 2", "is_active": False},
                    {"username": "test user 3", "is_superuser": True},
                ],
                ["test user 1", "test user 2"],
                {},
                ["test user 1", "test user 3"],
            ),
            (
                [
                    {"username": "test user 1"},
                    {"username": "test user 2", "is_active": False},
                    {"username": "test user 3", "is_superuser": True},
                ],
                ["test user 1", "test user 2"],
                {"is_active": True, "include_superusers": False},
                ["test user 1"],
            ),
            (
                [
                    {"username": "test user 1"},
                    {"username": "test user 2", "is_active": False},
                    {
                        "username": "test user 3",
                        "is_superuser": True,
                        "is_active": False,
                    },
                ],
                ["test user 1", "test user 2"],
                {"is_active": False, "include_superusers": True},
                ["test user 2", "test user 3"],
            ),
            (
                [
                    {"username": "test user 1"},
                    {"username": "test user 2", "is_active": False},
                    {"username": "test user 3", "is_superuser": True},
                ],
                ["test user 1", "test user 2"],
                {"is_active": None},
                ["test user 1", "test user 2", "test user 3"],
            ),
        ],
    )
    def test_with_role(
        self,
        user_data_list,
        users_with_role,
        with_role_kwargs,
        expected_usernames_with_role,
        role,
    ):
        for user_data in user_data_list:
            user = CustomUser.objects.create(**user_data)
            if user.username in users_with_role:
                user.roles.set([role])
                print(user.roles.all())

        assert set(
            CustomUser.with_role(role, **with_role_kwargs).values_list(
                "username", flat=True
            )
        ) == set(expected_usernames_with_role)
        assert set(
            CustomUser.with_role(role.name, **with_role_kwargs).values_list(
                "username", flat=True
            )
        ) == set(expected_usernames_with_role)

    def test_with_role_invalid_role_argument(self):
        with pytest.raises(
            TypeError, match="The `role` argument must be a string or a Role instance."
        ):
            CustomUser.with_role(1)

    @pytest.mark.parametrize(
        "role_data_list,expected_roles",
        [
            (
                [],
                set(),
            ),
            (
                [
                    {"name": "test_role1"},
                ],
                {"test_role1"},
            ),
            (
                [
                    {"name": "test_role1"},
                    {"name": "test_role2"},
                ],
                {"test_role1", "test_role2"},
            ),
        ],
    )
    def test_get_roles(self, role_data_list, expected_roles, user):
        user_roles = []
        for role_data in role_data_list:
            user_roles.append(Role.objects.create(**role_data))

        user.roles.set(user_roles)

        assert user.get_roles() == expected_roles
