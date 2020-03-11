from brick.processor import BrickProcessor

from bricksdk import BrickFactory
from bricksdk.brick_processors import InputBrickProcessor
from bricksdk.utils import Environments

brick_factory = BrickFactory(environment=Environments.DEBUG_ENV).add_brick_processor(brick_processor=BrickProcessor())
brick = brick_factory.create_brick(is_input_brick=True)
brick.initialize_components()
# TODO remove the below line to use the proper brick runner, dummy brick runner only lets you visualize brick invoke
#  procedure
brick_factory.add_dummy_brick_runner()
# TODO Remove the blow 2 lines as well it only lets you
input_processor = InputBrickProcessor(brick=brick)
result = input_processor.process(inputs=["Hello"])
print(result)
brick.start()
