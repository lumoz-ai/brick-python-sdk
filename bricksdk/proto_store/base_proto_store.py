import inspect
import os
import abc
import shutil

from ..connectors.grpc.proto_processor.processor import ProtoUtils


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

    def __init__(self, *args, proto_store_config, project_proto_directory="protos", **kwargs):
        super().__init__(proto_store_config, *args, **kwargs)
        self.module_director = self._get_module_directory()
        self.project_proto_directory = project_proto_directory

    def _get_module_directory(self):
        current_class_path = inspect.getfile(self.__class__)
        return current_class_path[:current_class_path.rfind("/")]

    def register_proto(self, proto_file_path: str):
        store_location = self.get_store_location()
        proto_file_names = os.listdir(store_location)
        new_proto_id = len(proto_file_names) + 1
        proto_file_name = proto_file_path[proto_file_path.rfind("/") + 1:]
        dot_index = proto_file_name.rfind(".")
        proto_file_name = "{}_{}.{}".format(proto_file_name[:dot_index], new_proto_id, proto_file_name[dot_index + 1:])
        new_proto_file_path = os.path.join(store_location, proto_file_name)
        shutil.copy(proto_file_path, new_proto_file_path)
        return new_proto_id

    def get_proto_from_store(self, proto_id):
        store_location = self.get_store_location()
        proto_file_names = os.listdir(store_location)
        for proto_file_name in proto_file_names:
            if proto_file_name.endswith("{}.proto".format(proto_id)):
                self.copy_dependencies_for(proto_file_name)
                proto_file_path = os.path.join(self.project_proto_directory, proto_file_name)
                return proto_file_name, proto_file_path
        return None, None

    def get_store_location(self):
        return os.path.join(self.module_director, self.proto_store_config.store_location)

    def copy_dependencies_for(self, proto_file_name):
        store_location = self.get_store_location()
        dependencies = ProtoUtils.get_dependencies_for_proto(input_directory=store_location,
                                                             proto_file_name=proto_file_name)
        for dependency in dependencies:
            self.copy_dependencies_for(dependency)
        source_proto_file_path = os.path.join(store_location, proto_file_name)
        shutil.copy(source_proto_file_path, self.project_proto_directory)
