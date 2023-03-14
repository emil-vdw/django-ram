"""Test the role definition module."""
import pytest
from django.core.management import call_command

from django_ram import definition
from django_ram.models import Role


@pytest.fixture
def clear_roles():
    Role.objects.all().delete()


@pytest.fixture(autouse=True)
def reset_role_definitions():
    original_definitions = definition.role_definitions.copy()
    yield
    definition.role_definitions = original_definitions


class TestRoleDefinition:
    def test_role_definition_registered(self):
        assert "test_role" not in [
            role_definition.name for role_definition in definition.role_definitions
        ]

        class TestRole(definition.RoleDefinition):
            name = "test_role"

        assert "test_role" in [
            role_definition.name for role_definition in definition.role_definitions
        ]

    def test_role_definition_missing_required_attributes(self):
        with pytest.raises(
            AssertionError,
            match="Role definition 'TestRole' is missing required attribute 'name'",
        ):

            class TestRole(definition.RoleDefinition):
                pass

    @pytest.mark.django_db
    def test_roles_created_post_migration(self, clear_roles):
        class TestRole(definition.RoleDefinition):
            name = "test_role"
            description = "Some obscure description"

        call_command("migrate", "--noinput")

        # Roles defined in ‘roles.py’
        assert Role.objects.filter(name="Author").exists()
        assert Role.objects.filter(name="Admin").exists()

        assert Role.objects.filter(
            name="test_role", description="Some obscure description"
        ).exists()

    @pytest.mark.django_db
    def test_role_definition_updated(self):
        Role.objects.create(
            name="test_role",
            description="Some obscure description",
        )

        class TestRole(definition.RoleDefinition):
            name = "test_role"
            description = "Some even more obscure description"

        call_command("migrate", "--noinput")

        assert (
            Role.objects.filter(
                name="test_role", description="Some obscure description"
            ).exists()
            is False
        )
        assert Role.objects.filter(
            name="test_role", description="Some even more obscure description"
        ).exists()

    @pytest.mark.django_db
    def test_removed_roles_marked_inactive(self):
        Role.objects.create(
            name="removed_role",
            description="No longer defined",
        )
        call_command("migrate", "--noinput")

        assert Role.objects.get(name="removed_role").active is False

    @pytest.mark.django_db
    def test_removed_roles_deleted(self, settings):
        settings.DELETE_REMOVED_ROLES = True
        Role.objects.create(
            name="removed_role",
            description="No longer defined",
        )
        call_command("migrate", "--noinput")

        assert Role.objects.filter(name="removed_role").exists() is False

    def test_role_definition_duplicate_name(self):
        class TestRole(definition.RoleDefinition):
            name = "test_role"
            description = "Some obscure description"

        with pytest.raises(
            AssertionError,
            match="Role definition 'DuplicateTestRole' has role name 'test_role' that already exists",
        ):

            class DuplicateTestRole(definition.RoleDefinition):
                name = "test_role"
