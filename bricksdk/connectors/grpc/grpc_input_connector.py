from concurrent import futures

import grpc

from ..base_connector import BaseInputConnector
from .proto_processor import Processor


class GrpcInputConnector(BaseInputConnector):

    def __init__(self, proto_file_path, config, brick_processor):
        super().__init__()
        self.config = config
        self.brick_processor = brick_processor
        self.processor = Processor(proto_file_path)
        self.server = None
        self.server_url = None

    def initialize(self, *args, **kwargs):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        GrpcInterface = self._build_grpc_interface()
        self.processor.get_add_servicer_method()(GrpcInterface(), self.server)
        self.server_url = "[::]:{}".format(self.config.grpc.port)
        self.server.add_insecure_port(self.server_url)

    def listen(self, request, context):
        return self.brick_processor.process(request, context)
        # return request

    def start(self, *args, **kwargs):
        print("Starting brick connector on {}".format(self.server_url))
        self.server.start()
        self.server.wait_for_termination()

    def _build_grpc_interface(self):
        method_name = self.processor.get_rpc_method_name()
        members = {method_name: self.listen}
        GrpcInterface = type("GrpcInterface", (self.processor.get_servicer(),), members)
        return GrpcInterface
