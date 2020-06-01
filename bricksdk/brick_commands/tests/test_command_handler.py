import unittest
from bricksdk.brick_commands.command_handler import BrickCommandHandler
from bricksdk.brick_commands import proto
from unittest.mock import patch

import sys
print(sys.modules[__name__])
class TestCommandHandler(unittest.TestCase):
    class Commands:
        def __init__(self, command, name, download, set_as_input, compile):
            self.command = command
            self.name = name
            self.download = download
            self.set_as_input = set_as_input
            self.compile = compile

    def test_with_all_arguments_none(self):
        commands = self.Commands(None, None, None, None, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        test_output = brick_command_handler.execute_commands()
        self.assertEqual(None, test_output)

    def test_with_command_create(self):
        commands = self.Commands("create", "name", True, True, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        self.assertRaises(TypeError, brick_command_handler.execute_commands)

    def test_with_command_initialize(self):
        commands = self.Commands("initialize", "name", True, True, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        test_output = brick_command_handler.execute_commands()
        self.assertEqual(None, test_output)

    @patch('bricksdk.brick_commands.proto.download_proto')
    def test_with_command_proto_download(self, mock_download_proto):
        commands = self.Commands("proto", "name", True, True, False)
        brick_command_handler=BrickCommandHandler(command_line_arguments=commands)
        brick_command_handler.execute_commands()
        self.assertTrue(mock_download_proto.called)
        mock_download_proto.assert_called_once()

    @patch('bricksdk.brick_commands.proto.compile_proto')
    def test_with_command_proto_compile(self, mock_compile_proto):
        commands = self.Commands("proto", "name", False, False, True)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        brick_command_handler.execute_commands()
        self.assertTrue(mock_compile_proto.called)
        mock_compile_proto.assert_called_once()

    def test_with_name_none(self):
        commands = self.Commands("create", None, True, True, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        self.assertRaises(TypeError, brick_command_handler.execute_commands)

    def test_with_download_none(self):
        commands = self.Commands("create", "name", None, True, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        self.assertRaises(TypeError, brick_command_handler.execute_commands)

    def test_with_compile_none(self):
        commands = self.Commands("create", "name", True, True, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        self.assertRaises(TypeError, brick_command_handler.execute_commands)

    def test_with_set_as_input_none(self):
        commands = self.Commands("create", "name", True, None, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        self.assertRaises(TypeError, brick_command_handler.execute_commands)

    def test_with_proper_command_arguments(self):
        commands = self.Commands("create", "name", True, True, None)
        brick_command_handler = BrickCommandHandler(command_line_arguments=commands)
        pass
