import unittest
from bricksdk.brick_commands.tests.test_command_handler import TestCommandHandler
from bricksdk.brick_commands.tests.test_create import TestCreate

test_command_handler = unittest.TestLoader().loadTestsFromTestCase(TestCommandHandler)
test_create = unittest.TestLoader().loadTestsFromTestCase(TestCreate)

runTest = unittest.TestSuite([test_command_handler, test_create])

unittest.TextTestRunner(verbosity=2).run(runTest)
