import logging

from .base_brick_runner import BaseBrickRunner
from bricksdk.connectors import get_output_connector
from ...proto_store import FileBasedProtoStore


class BrickRunner(BaseBrickRunner):

    def __init__(self, brick_name, brick_config):
        super().__init__(brick_name, brick_config)
        logging.debug("Initialized connection to {} with configuration {}".format(brick_name, brick_config))
        self.proto_store = FileBasedProtoStore(proto_store_config=self.brick_config.proto_store_configuration)
        _, self.proto_file_path = self.proto_store.get_proto_from_store(self.brick_config.brick.input_proto_id)
        self.output_connector = get_output_connector(config=self.brick_config, proto_file_path=self.proto_file_path)
        self.output_connector.start()

    def _execute(self, *args, force_rerun=False, **kwargs):
        return self.output_connector.send(self.proto)
