import grpc

from .proto_processor import Processor
from ..base_connector import BaseOutputConnector


class GrpcOutputConnector(BaseOutputConnector):

    def __init__(self, proto_file_path):
        super().__init__()
        self.processor = Processor(proto_file_path)
        self.Stub = None
        self.stub = None
        self.channel = None

    def initialize(self, *args, **kwargs):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.Stub = self.processor.get_stub()

    def send(self, message):
        method_name = self.processor.get_rpc_method_name()
        return self.stub.__dict__[method_name](message)

    def start(self, *args, **kwargs):
        self.stub = self.Stub(self.channel)
