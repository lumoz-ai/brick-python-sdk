from .base_brick_runner import BaseBrickRunner
from bricksdk.connectors import get_output_connector


class BrickRunner(BaseBrickRunner):

    def __init__(self, brick_name, brick_config):
        super().__init__(brick_name, brick_config)
        self.proto_file_path = self.brick_config.brick.proto_file_path
        self.output_connector = get_output_connector(config=self.brick_config, proto_file_path=self.proto_file_path)
        self.output_connector.start()

    def _execute(self, *args, force_rerun=False, **kwargs):
        return self.output_connector.send(self.proto)
