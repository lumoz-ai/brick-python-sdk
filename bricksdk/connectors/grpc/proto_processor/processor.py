import abc
import os
import re
from concurrent import futures
from importlib import import_module

import grpc
from grpc_tools import protoc


class Builder(abc.ABC):

    def __init__(self, proto_file_path, brick_processor):
        self.processor = Processor(proto_file_path)
        self.brick_processor = brick_processor

    def build_server(self, config):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        GrpcInterface = self._build_grpc_interface()
        self.processor.get_add_servicer_method()(GrpcInterface(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

    def build_client(self, config):
        channel = grpc.insecure_channel('localhost:50051')
        stub = self.processor.get_stub()(channel)
        return stub

    def _build_grpc_interface(self):
        method, method_name = self.processor.get_rpc_method_name()
        members = {method_name: self.processor.process}
        GrpcInterface = type("GrpcInterface", (self.processor.get_servicer(),), members)
        return GrpcInterface


class Processor(abc.ABC):
    RPC_FROM_PROTO_FILE_REGEX = r"rpc \w+\(\w+\) returns \(\w+\)"
    RPC_NAME_REGEX = r"rpc \w+"
    ADD_SERVICER_TO_SERVER_REGEX = r"add_\w+_to_server"
    STUB_REGEX = r"\w+Stub"
    SERVIER_REGEX = r"\w+Servicer"

    def __init__(self, proto_file_path):
        self.parser = Parser(proto_file_path)
        self.proto_file_path = proto_file_path
        self.add_servicer_method = None
        self.pb_file_content = None
        self.grpc_file_content = None
        self.proto_file_content = None
        self.servicer = None
        self.stub = None

    def get_rpc_method_name(self):
        rpc_string = re.findall(self.RPC_NAME_REGEX, self._get_proto_file_content())[0]
        method_name = rpc_string.split(" ")[-1]
        return method_name

    def _get_proto_file_content(self):
        if self.proto_file_content is None:
            self.proto_file_content = open(self.proto_file_path, "r").read()
        return self.proto_file_content

    def get_servicer(self):
        if self.servicer is None:
            pb, grpc = self.parser.get_pb_and_grpc()
            servicer_name = self._get_servicer_name()
            self.servicer = getattr(grpc, servicer_name)
        return self.servicer

    def get_add_servicer_method(self):
        if self.add_servicer_method is None:
            pb, grpc = self.parser.get_pb_and_grpc()
            add_servicer_method_name = self._get_add_servicer_method_name()
            add_servicer_method = getattr(grpc, add_servicer_method_name)
            return add_servicer_method
        return self.add_servicer_method

    def get_stub(self):
        if self.stub is None:
            pb, grpc = self.parser.get_pb_and_grpc()
            stub_name = self._get_stub_name()
            self.stub = getattr(grpc, stub_name)
        return self.stub

    def _get_add_servicer_method_name(self):
        add_servicer_method_name = re.findall(self.ADD_SERVICER_TO_SERVER_REGEX, self._get_grpc_file_content())[0]
        return add_servicer_method_name

    def _get_servicer_name(self):
        add_servicer_name = re.findall(self.SERVIER_REGEX, self._get_grpc_file_content())[0]
        return add_servicer_name

    def _get_stub_name(self):
        stub_name = re.findall(self.STUB_REGEX, self._get_grpc_file_content())[0]
        return stub_name

    def _get_grpc_file_content(self):
        if self.grpc_file_content is None:
            self.grpc_file_content = open(self.parser.get_grpc_python_file(), "r").read()
        return self.grpc_file_content

    def _get_pb_file_content(self):
        if self.pb_file_content is None:
            self.pb_file_content = open(self.parser.get_pb_python_file(), "r").read()
        return self.pb_file_content


class Parser(abc.ABC):
    PROTO_TEMPLATE = "{}_pb2"
    GRPC_TEMPLATE = "{}_pb2_grpc"

    def __init__(self, proto_file_path, input_directory="protos", output_directory="protos"):
        self.proto_file_path = proto_file_path
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.proto_file_name = None
        self.proto_name = None
        self.pb_module = None
        self.grpc_module = None
        self.pb_python_file = None
        self.grpc_python_file = None
        self._initialize()

    def _initialize(self):
        split_index = self.proto_file_path.rfind("/")
        self.output_directory = "protos"
        if split_index > 0:
            self.proto_file_name = self.proto_file_path[(split_index + 1):]
            self.input_directory = self.proto_file_path[:split_index]
        else:
            self.proto_file_name = self.proto_file_path
            self.proto_input_directory = "."
        self.proto_name = self.proto_file_name.split(".")[0]

    def compile_proto(self):
        # Create pb2
        protoc.main(["-m grpc_tools.protoc", "-I={}".format(self.input_directory),
                     "--python_out={}".format(self.output_directory), self.proto_file_name])
        # Create pb2_grpc
        protoc.main(["-m grpc_tools.protoc", "-I={}".format(self.input_directory),
                     "--grpc_python_out={}".format(self.output_directory), self.proto_file_name])
        with open(os.path.join(self.output_directory, "__init__.py"), "w") as _:
            pass
        self.fix_pb_import()

    def fix_pb_import(self):
        command = "sed -i -E 's/^import.*_pb2/from . \\0/' {}/{}.py".format(self.output_directory,
                                                                            self.get_grpc_file_name())
        os.system(command)

    def get_pb_and_grpc(self):
        if self.pb_module is None:
            self.pb_module = import_module("{}.{}".format(self.output_directory, self.get_pb_file_name()))
        if self.grpc_module is None:
            self.grpc_module = import_module("{}.{}".format(self.output_directory, self.get_grpc_file_name()))
        return self.pb_module, self.grpc_module

    def get_pb_file_name(self):
        return self.PROTO_TEMPLATE.format(self.proto_name)

    def get_grpc_file_name(self):
        return self.GRPC_TEMPLATE.format(self.proto_name)

    def get_relative_proto_path(self):
        return os.path.join(self.output_directory, self.get_grpc_file_name())

    def get_pb_python_file(self):
        return os.path.join(self.output_directory, "{}.py".format(self.get_pb_file_name()))

    def get_grpc_python_file(self):
        return os.path.join(self.output_directory, "{}.py".format(self.get_grpc_file_name()))
