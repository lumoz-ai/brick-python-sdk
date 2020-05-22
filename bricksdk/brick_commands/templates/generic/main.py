from bricksdk import BrickFactory
from bricksdk.utils import Environments

from brick.processor import BrickProcessor

brick_factory = BrickFactory(environment=Environments.DEBUG_ENV).add_brick_processor(brick_processor=BrickProcessor())
brick = brick_factory.create_brick()
brick.initialize_components()
brick.start()
