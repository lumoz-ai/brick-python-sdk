import json
import os

from brick.processor import BrickProcessor

from bricksdk import BrickFactory
from bricksdk.configurations import Configuration
from bricksdk.utils import Environments

json_configuration = None
if os.environ.get("configuration"):
    json_configuration = json.loads(os.environ.get("configuration"))
configuration = Configuration(environment=Environments.DEBUG_ENV).load(json_configuration)

brick_factory = BrickFactory(environment=Environments.DEBUG_ENV, configuration=configuration).add_brick_processor(
    brick_processor=BrickProcessor())
brick = brick_factory.create_brick()
brick.initialize_components()
brick.start()
