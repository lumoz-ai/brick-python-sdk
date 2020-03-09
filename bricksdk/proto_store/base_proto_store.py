import os
import abc
import shutil


class BaseProtoStore(abc.ABC):

    def __init__(self, proto_store_config, *args, **kwargs):
        self.proto_store_config = proto_store_config

    @abc.abstractmethod
    def register_proto(self, proto_file_path):
        pass

    @abc.abstractmethod
    def get_proto_from_store(self, proto_id):
        pass


class FileBasedProtoStore(BaseProtoStore):
    def register_proto(self, proto_file_path: str):
        proto_file_names = os.listdir(self.proto_store_config.store_location)
        new_proto_id = len(proto_file_names) + 1
        proto_file_name = proto_file_path[proto_file_path.rfind("/") + 1:]
        dot_index = proto_file_name.rfind(".")
        proto_file_name = "{}_{}.{}".format(proto_file_name[:dot_index], new_proto_id, proto_file_name[dot_index + 1:])
        new_proto_file_path = os.path.join(self.proto_store_config.store_location, proto_file_name)
        shutil.copy(proto_file_path, new_proto_file_path)
        return new_proto_id

    def get_proto_from_store(self, proto_id):
        proto_file_names = os.listdir(self.proto_store_config.store_location)
        for proto_file_name in proto_file_names:
            if proto_file_name.endswith("{}.proto".format(proto_id)):
                proto_file_path = os.path.join(self.proto_store_config.store_location, proto_file_name)
                return proto_file_name, proto_file_path
        return None, None
