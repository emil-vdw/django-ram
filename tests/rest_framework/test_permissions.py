from unittest.mock import Mock

import pytest

from django_ram.models import Role
from django_ram.rest_framework.permissions import (
    HasRoleBasePermission,
    generate_permission_name_from_role_definition,
    has_role,
)
from tests.test_roles.roles import Administrator, Author


@pytest.fixture
def author(django_user_model):
    user = django_user_model.objects.create(
        username="test_user", password="test_password"
    )
    user.roles.add(Role.objects.get(name="Author"))
    return user


class TestGeneratePermissionName:
    @pytest.mark.parametrize(
        "role_name,expected_permission_class_name",
        [
            ("article_proof_reader", "HasArticleProofReaderRole"),
            ("article_proof_reader_role", "HasArticleProofReaderRole"),
            ("Article Proof Reader", "HasArticleProofReaderRole"),
            ("Article Proof Reader Role", "HasArticleProofReaderRole"),
        ],
    )
    def test_generate_permission_name_from_role_definition(
        self, role_name, expected_permission_class_name
    ):
        mock_role_definition = Mock()
        mock_role_definition.name = role_name

        assert (
            generate_permission_name_from_role_definition(mock_role_definition)
            == expected_permission_class_name
        )


@pytest.mark.django_db
class TestHasRoleFactory:
    class HasAuthorRole(HasRoleBasePermission):
        role_definition = Author

    class HasAdminRole(HasRoleBasePermission):
        role_definition = Administrator

    @pytest.mark.parametrize(
        "permission_class,should_have_permission,should_have_object_permission",
        [
            #  Using the `has_role` permission class factory.
            (has_role(Author), True, True),
            (has_role(Administrator) | has_role(Author), True, True),
            (has_role(Administrator) | has_role(Author), True, True),
            (~has_role(Administrator), True, True),
            (has_role(Administrator), False, False),
            (~has_role(Author), False, False),
            (has_role(Administrator) & has_role(Author), False, False),
            #  Inherited from base permission class.
            (HasAuthorRole, True, True),
            (HasAdminRole | HasAuthorRole, True, True),
            (HasAdminRole | HasAuthorRole, True, True),
            (~HasAdminRole, True, True),
            (HasAdminRole, False, False),
            (~HasAuthorRole, False, False),
            (HasAdminRole & HasAuthorRole, False, False),
        ],
    )
    def test_user_has_role_permission_class(
        self,
        permission_class,
        should_have_permission,
        should_have_object_permission,
        author,
    ):
        mock_request = Mock(user=author)
        mock_view = Mock()
        mock_object = Mock()

        permission_class_instance = permission_class()

        assert (
            permission_class_instance.has_permission(mock_request, mock_view)
            == should_have_permission
        )
        assert (
            permission_class_instance.has_object_permission(
                mock_request, mock_view, mock_object
            )
            == should_have_object_permission
        )
