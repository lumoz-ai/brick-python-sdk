import os

from ..configurations import Configuration
from ..connectors.grpc.proto_processor.processor import ProtoCompiler
from ..proto_store import FileBasedProtoStore


def download_proto():
    configuration = Configuration(environment="debug").load()
    proto_store = FileBasedProtoStore(proto_store_config=configuration.proto_store_configuration)
    proto_store.get_proto_from_store(proto_id=configuration.brick.input_proto_id)
    proto_store.get_proto_from_store(proto_id=configuration.brick.output_proto_id)


def compile_proto():
    proto_compiler = ProtoCompiler(proto_file_name="", input_directory="protos", output_directory="protos")
    proto_file_names = os.listdir("protos")
    for proto_file_name in proto_file_names:
        proto_compiler.proto_file_name = proto_file_name
        proto_compiler.compile()
