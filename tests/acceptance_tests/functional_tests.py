from unittest import TestCase

from tests.acceptance_tests.driver import Driver
from tests.acceptance_tests.dsl import Dsl


class FunctionalTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(FunctionalTests, self).__init__(*args, **kwargs)
        self.dsl = Dsl(Driver(base_url="https://localhost/"))

    def setUp(self):
        self.dsl.setup()

    def tearDown(self):
        self.dsl.tear_down()

    def test_create_register_name_required(self):
        self.dsl.create_new_register(name="")
        self.dsl.confirm_name_required_validation_error()

    def test_create_register_name_must_be_unique(self):
        self.dsl.ensure_existing_register(name="Existing register")
        self.dsl.create_new_register(name="Existing register")
        self.dsl.confirm_name_already_exists_validation_error()

    def test_can_create_new_register(self):
        self.dsl.create_new_register()
        self.dsl.confirm_register_created()

    def test_can_view_register(self):
        self.dsl.ensure_existing_register()
        self.dsl.confirm_can_view_register()

    def test_edit_register_name_required(self):
        self.dsl.ensure_existing_register()
        self.dsl.update_existing_register(new_name="")
        self.dsl.confirm_name_required_validation_error()

    def test_edit_register_name_must_be_unique(self):
        self.dsl.ensure_existing_register(name="Existing register")
        self.dsl.create_new_register(name="Another register")
        self.dsl.update_existing_register(current_name="Another register", new_name="Existing register")
        self.dsl.confirm_name_already_exists_validation_error()

    def test_can_edit_register(self):
        self.dsl.ensure_existing_register(name="Old")
        self.dsl.update_existing_register(current_name="Old", new_name="New")
        self.dsl.confirm_register_updated(old_name="Old", new_name="New")

    def test_can_delete_register(self):
        self.dsl.ensure_existing_register()
        self.dsl.delete_existing_register()
        self.dsl.confirm_register_deletion_requires_confirmation()
        self.dsl.confirm_register_deletion()
        self.dsl.confirm_register_deleted()

    def test_can_cancel_delete_register(self):
        self.dsl.ensure_existing_register()
        self.dsl.delete_existing_register()
        self.dsl.confirm_register_deletion_requires_confirmation()
        self.dsl.cancel_register_deletion()
        self.dsl.confirm_register_exists()

    def test_add_entry_name_required(self):
        self.dsl.ensure_existing_register()
        self.dsl.add_entry_to_register(entry_name="")
        self.dsl.confirm_name_required_validation_error()

    def test_add_entry_name_must_be_unique(self):
        self.dsl.ensure_existing_register()
        self.dsl.ensure_existing_entry(entry_name="Existing entry")
        self.dsl.add_entry_to_register(entry_name="Existing entry")
        self.dsl.confirm_name_already_exists_validation_error()

    def test_can_add_entry(self):
        self.dsl.ensure_existing_register()
        self.dsl.add_entry_to_register()
        self.dsl.confirm_entry_added()

    def test_entry_with_same_name_allowed_in_different_registers(self):
        self.dsl.ensure_existing_register("Register A")
        self.dsl.ensure_existing_register("Register B")
        self.dsl.ensure_existing_entry(register="Register A", entry_name="Entry 1")
        self.dsl.add_entry_to_register(register="Register B", entry_name="Entry 1")
        self.dsl.confirm_entry_added(register="Register B", entry_name="Entry 1")

    def test_can_view_entry(self):
        self.dsl.ensure_existing_register()
        self.dsl.ensure_existing_entry()
        self.dsl.confirm_can_view_entry()

    def test_can_edit_entry(self):
        self.dsl.ensure_existing_register()
        self.dsl.ensure_existing_entry(entry_name="Old")
        self.dsl.update_existing_entry(current_name="Old", new_name="New")
        self.dsl.confirm_entry_updated(old_name="Old", new_name="New")

    def test_can_delete_entry(self):
        self.dsl.ensure_existing_register()
        self.dsl.ensure_existing_entry()
        self.dsl.delete_existing_entry()
        self.dsl.confirm_entry_deletion_requires_confirmation()
        self.dsl.confirm_entry_deletion()
        self.dsl.confirm_entry_deleted()

    def test_can_cancel_delete_entry(self):
        self.dsl.ensure_existing_register()
        self.dsl.ensure_existing_entry()
        self.dsl.delete_existing_entry()
        self.dsl.confirm_entry_deletion_requires_confirmation()
        self.dsl.cancel_entry_deletion()
        self.dsl.confirm_entry_exists()