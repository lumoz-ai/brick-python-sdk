import os
import shutil
import unittest
from template_store.simple_template_store import SimpleTemplateStore
from bricksdk.brick_commands import create


class TestCreate(unittest.TestCase):
    def setUp(self):
        self.simple_template_store = SimpleTemplateStore(
            template_store_url="https://github.com/lumoz-ai/lumoz-brick-template-store/blob/develop/templates")

    def test_create(self):
        test_output = create.create(brick_name="name",
                                    set_as_input=True,
                                    template_folder="../templates"
                                    )
        self.assertTrue(test_output)

    def test_initialise(self):
        test_output = create.initialize(brick_name="name",
                                        set_as_input=True,
                                        template_folder="../templates",
                                        )
        self.assertTrue(test_output)

    def test_get_template_directory_with_set_as_input_true(self):
        test_output = create.get_template_directory(True, "./")
        self.assertEqual(os.path.join("./", "input"), test_output)

    def test_get_template_directory_with_set_as_input_false(self):
        test_output = create.get_template_directory(False, "./")
        self.assertEqual(os.path.join("./", "generic"), test_output)

    def test_copy(self):
        print(os.getcwd())
        create.copy(source_directory=".",destination_directory="../test_folder")
        self.assertTrue(os.path.exists("../test_folder"))
        shutil.rmtree("../test_folder")
