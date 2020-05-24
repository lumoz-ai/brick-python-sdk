import json
import os

from brick.processor import BrickProcessor

from bricksdk import BrickFactory
from bricksdk.configurations import Configuration
from bricksdk.brick_processors import InputBrickProcessor
from bricksdk.utils import Environments

json_configuration = json.load(open("configurations/debug.json", "r"))
if os.environ.get("configuration"):
    json_configuration = json.loads(os.environ.get("configuration"))
if os.environ.get("graph_configuration"):
    json_configuration["graph_configuration"] = json.loads(os.environ.get("graph_configuration"))
if os.environ.get("graph"):
    json_configuration["graph"] = json.loads(os.environ.get("graph"))
if os.environ.get("input_brick_names"):
    json_configuration["meta"]["input_brick_names"] = json.loads(os.environ.get("input_brick_names"))
if os.environ.get("output_brick_names"):
    json_configuration["meta"]["output_brick_names"] = json.loads(os.environ.get("output_brick_names"))
configuration = Configuration(environment=Environments.DEBUG_ENV).load(json_configuration)
configuration.meta_store_api = os.environ.get("meta_store_api", "http://0.0.0.0:3000/v1/artefacts")

brick_factory = BrickFactory(environment=Environments.DEBUG_ENV, configuration=configuration).add_brick_processor(
    brick_processor=BrickProcessor())
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
