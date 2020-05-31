import os
import unittest
from unittest.mock import patch

from bricksdk.brick_processors.input_brick_processor import InputBrickProcessor
from bricksdk.brick_processors.base_brick_processor import BaseBrickProcessor
import abc


class TestBrickProcessor(unittest.TestCase):

    @patch('bricksdk.base_brick.BaseBrick.execute')
    def test_execution_of_brick(self, mock_base_brick_execute):
        base_brick_processor = BaseBrickProcessor(abc.ABC)
        input_brick_processor = InputBrickProcessor(base_brick_processor)
        test_output = input_brick_processor.process()
        self.assertTrue(mock_base_brick_execute.called)
        mock_base_brick_execute.assert_called_once()
