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
    RPC_FROM_PROTO_FILE_REGEX = r"rpc\w+\(\w+\)returns\(\w+\)"
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

    def get_rpc_declaration(self):
        rpc_string = re.findall(self.RPC_FROM_PROTO_FILE_REGEX, self._get_proto_file_content().replace(" ", ""))
        return rpc_string

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
        self.proto_name = ProtoUtils.get_proto_name_from_proto_file_name(proto_file_name=self.proto_file_name)

    def get_pb_and_grpc(self):
        folders = self.output_directory.split("/")
        protos_module = ".".join(folders)
        if self.pb_module is None:
            self.pb_module = import_module(
                "{}.{}".format(protos_module, ProtoUtils.get_pb_file_name(proto_name=self.proto_name)))
        if self.grpc_module is None:
            self.grpc_module = import_module("{}.{}".format(protos_module,
                                                            ProtoUtils.get_grpc_file_name(proto_name=self.proto_name)))
        return self.pb_module, self.grpc_module

    def get_relative_proto_path(self):
        return os.path.join(self.output_directory, ProtoUtils.get_grpc_file_name(proto_name=self.proto_name))

    def get_pb_python_file(self):
        return os.path.join(self.output_directory,
                            "{}.py".format(ProtoUtils.get_pb_file_name(proto_name=self.proto_name)))

    def get_grpc_python_file(self):
        return os.path.join(self.output_directory,
                            "{}.py".format(ProtoUtils.get_grpc_file_name(proto_name=self.proto_name)))


class ProtoUtils:
    PROTO_TEMPLATE = "{}_pb2"
    GRPC_TEMPLATE = "{}_pb2_grpc"
    IMPORT_STATEMENT_REGEX = r"\"\w+.proto\""

    @staticmethod
    def get_pb_file_name(*, proto_name):
        return ProtoUtils.PROTO_TEMPLATE.format(proto_name)

    @staticmethod
    def get_grpc_file_name(*, proto_name):
        return ProtoUtils.GRPC_TEMPLATE.format(proto_name)

    @staticmethod
    def get_proto_name_from_proto_file_name(*, proto_file_name):
        return proto_file_name.split(".")[0]

    @staticmethod
    def get_dependencies_for_proto(*, input_directory, proto_file_name):
        proto_file_path = os.path.join(input_directory, proto_file_name)
        proto_file_content = open(proto_file_path, "r").read()
        import_statements = re.findall(ProtoUtils.IMPORT_STATEMENT_REGEX, proto_file_content)
        import_proto_names = list(map(lambda import_statement: import_statement[1:-1], import_statements))
        return import_proto_names


class ProtoCompiler:

    def __init__(self, *, proto_file_name, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.proto_file_name = proto_file_name

    def compile(self):
        self._compile(self.proto_file_name)
        grpc_file_name = ProtoUtils.get_grpc_file_name(
            proto_name=ProtoUtils.get_proto_name_from_proto_file_name(
                proto_file_name=self.proto_file_name))
        pb_file_name = ProtoUtils.get_pb_file_name(
            proto_name=ProtoUtils.get_proto_name_from_proto_file_name(proto_file_name=self.proto_file_name))
        self.fix_pb_import(grpc_file_name)
        self.fix_pb_import(pb_file_name)

    def _compile(self, proto_file_name):
        print("Compiling {}".format(proto_file_name))
        dependencies = ProtoUtils.get_dependencies_for_proto(input_directory=self.input_directory,
                                                             proto_file_name=proto_file_name)
        for dependency in dependencies:
            self._compile(dependency)
        self.compile_proto(proto_file_name=proto_file_name)

    def compile_proto(self, *, proto_file_name):
        # Create pb2
        protoc.main(["-m grpc_tools.protoc", "-I={}".format(self.input_directory),
                     "--python_out={}".format(self.output_directory), proto_file_name])
        # Create pb2_grpc
        protoc.main(["-m grpc_tools.protoc", "-I={}".format(self.input_directory),
                     "--grpc_python_out={}".format(self.output_directory), proto_file_name])
        with open(os.path.join(self.output_directory, "__init__.py"), "w") as _:
            pass

    def fix_pb_import(self, grpc_file_name):
        command = "sed -i -E 's/^import.*_pb2/from . \\0/' {}/{}.py".format(self.output_directory,
                                                                            grpc_file_name)
        os.system(command)
