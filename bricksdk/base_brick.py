from abc import ABC

from .configurations import Configuration
from .connectors.grpc.grpc_input_connector import GrpcInputConnector
from .connectors.grpc.grpc_output_connector import GrpcOutputConnector
from .observer import Publisher
from .proto_store import FileBasedProtoStore
from .solution_runner.brick_runner.base_brick_runner import TestBrickRunner
from .solution_runner.simple_runner import SimpleRunner
from .utils import Environments, ABCSingleton


class BaseBrick(ABC, metaclass=ABCSingleton):

    def __init__(self, *args, **kwargs):
        self.input_proto_file = None
        self.output_proto_file = None
        self.input_names = []
        self.output_names = []
        self.proto_store = None
        self.input_connector = None
        self.output_connector = None
        self.configuration = None
        self.solution_runner = None
        self.event_registry = Publisher()

    def start(self):
        pass

    def initialize_components(self):
        self.input_connector.initialize()
        self.output_connector.initialize()

    def execute(self, inputs):
        return self.solution_runner.execute_graph(inputs=inputs)


class Brick(BaseBrick):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
        self.output_connector.start()
        self.input_connector.start()


class BrickFactory:

    def __init__(self, *args, environment=Environments.DEBUG_ENV, **kwargs):
        self.brick_processor = None
        # TODO refactor this logic
        self.configuration = kwargs.get("configuration") if kwargs.get("configuration") else Configuration(
            environment=environment).load()
        self.brick = Brick()
        self.brick.configuration = self.configuration

    def add_brick_processor(self, brick_processor):
        self.brick_processor = brick_processor
        return self

    def add_dummy_brick_runner(self, brick_runner_class=None):
        brick_runner_class = TestBrickRunner if brick_runner_class is None else brick_runner_class
        self.brick.solution_runner.brick_runner = brick_runner_class
        return self

    def add_proto_store(self):
        proto_store = FileBasedProtoStore(proto_store_config=self.configuration.proto_store_configuration)
        self.brick.proto_store = proto_store
        _, self.brick.input_proto_file = proto_store.get_proto_from_store(self.configuration.brick.input_proto_id)
        _, self.brick.output_proto_file = proto_store.get_proto_from_store(self.configuration.brick.output_proto_id)
        return self

    def add_grpc_input(self):
        grpc_input = GrpcInputConnector(proto_file_path=self.brick.input_proto_file, config=self.configuration,
                                        brick_processor=self.brick_processor)
        self.brick.input_connector = grpc_input
        return self

    def add_grpc_output(self):
        grpc_output = GrpcOutputConnector(proto_file_path=self.brick.output_proto_file, config=self.configuration)
        self.brick.output_connector = grpc_output
        return self

    def add_solution_runner(self, graph):
        solution_runner = SimpleRunner(input_brick_names=self.configuration.meta.input_brick_names,
                                       output_brick_names=self.configuration.meta.output_brick_names,
                                       graph_config=self.configuration.graph_configuration)
        solution_runner.generate_dependency_graph(graph)
        self.brick.solution_runner = solution_runner
        return self

    def create_brick(self, is_input_brick=False):
        self.add_proto_store()
        self.add_grpc_input()
        self.add_grpc_output()
        if is_input_brick:
            self.add_solution_runner(graph=self.configuration.graph.__dict__)
        return self.brick
