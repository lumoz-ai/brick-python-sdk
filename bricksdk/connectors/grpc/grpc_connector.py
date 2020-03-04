from ..base_connector import BaseConnector
from .grpc_input_connector import GrpcInputConnector
from .grpc_output_connector import GrpcOutputConnector


class GrpcConnector(BaseConnector):

    def __init__(self, config, brick_processor, input_proto_file_path, output_proto_file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.brick_processor = brick_processor
        self.input_proto_file_path = input_proto_file_path
        self.output_proto_file_path = output_proto_file_path

    def initialize_input_connector(self, *args, **kwargs):
        self.input_connector = GrpcInputConnector(proto_file_path=self.input_proto_file_path,
                                                  brick_processor=self.brick_processor, config=self.config)
        self.input_connector.initialize(*args, **kwargs)

    def initialize_output_connector(self, *args, **kwargs):
        self.output_connector = GrpcOutputConnector(proto_file_path=self.output_proto_file_path, config=self.config)
        self.output_connector.initialize(*args, **kwargs)
